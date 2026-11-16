#!/usr/bin/python3
"""
Oracle Tablespace Monitoring Plugin - Refactored Version
Monitors Oracle tablespaces with pagination support (25 tablespaces per page)
"""

import json
import os
import logging
import argparse
import time
import fcntl  # For file locking
from typing import List, Dict, Tuple, Optional
from logging.handlers import RotatingFileHandler
from itertools import chain
plugin_version = 1

def setup_logging():
    """Configure file logging with rotation"""
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "oracle_tablespace.log")

    handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=3)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


logger = setup_logging()


class QueryCache:
    """Manages cached query results with file locking"""

    def __init__(self, cache_ttl: int = 180):  # 3 minutes default
        self.cache_dir = os.path.join(os.path.dirname(__file__), "cache")
        os.makedirs(self.cache_dir, exist_ok=True)

        self.cache_file = os.path.join(self.cache_dir, "tablespace_cache.json")
        self.lock_file = os.path.join(self.cache_dir, "queries.lock")
        self.cache_ttl = cache_ttl  # Cache time-to-live in seconds
    
    def get_cache_file(self, update: str) -> str:
        """Returns file path for requested file"""
        return os.path.join(self.cache_dir, "{}_cache.json".format(update))

    def is_cache_valid(self) -> bool:
        """Check if cache exists and is not expired"""
        if not os.path.exists(self.cache_file):
            return False

        cache_age = time.time() - os.path.getmtime(self.cache_file)
        is_valid = cache_age < self.cache_ttl

        if is_valid:
            logger.info("Cache is valid (age: %.1f seconds)", cache_age)
        else:
            logger.info("Cache expired (age: %.1f seconds)", cache_age)

        return is_valid

    def read_cache(self, update: str) -> Optional[List[Tuple]]:
        """Read cached query results"""
        self.cache_file = self.get_cache_file(update)
        
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Convert back to list of tuples
                results = [tuple(row) for row in data["results"]]
                logger.info("Read %d rows from cache", len(results))
                return results
        except Exception as e:
            logger.error("Failed to read cache: %s", e)
            return None

    def write_cache(self, results: List[Tuple], update: str) -> None:
        """Write query results to cache"""
        self.cache_file = self.get_cache_file(update)
        
        try:
            # Convert tuples to lists for JSON serialization
            data = {"timestamp": time.time(), "results": [list(row) for row in results]}

            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f)

            logger.info("Wrote %d rows to cache", len(results))
        except Exception as e:
            logger.error("Failed to write cache: %s", e)

    def acquire_lock(self, timeout: int = 30) -> Optional[object]:
        """Acquire exclusive lock (returns lock file object or None)"""
        try:
            lock_fd = open(self.lock_file, "w", encoding="utf-8")

            # Try to acquire lock with timeout
            start_time = time.time()
            while True:
                try:
                    fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    logger.info("Acquired lock")
                    return lock_fd
                except (IOError, BlockingIOError):
                    # Lock is held by another process
                    if time.time() - start_time > timeout:
                        logger.warning("Lock timeout after %d seconds", timeout)
                        lock_fd.close()
                        return None

                    logger.debug("Waiting for lock...")
                    time.sleep(0.5)

        except Exception as e:
            logger.error("Failed to acquire lock: %s", e)
            return None

    def release_lock(self, lock_fd) -> None:
        """Release lock"""
        if lock_fd:
            try:
                fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)
                lock_fd.close()
                logger.info("Released lock")
            except Exception as e:
                logger.error("Failed to release lock: %s", e)


class OracleMonitor:
    """Handles Oracle database connections"""

    def __init__(
        self,
        hostname: str,
        port: str,
        sid: str,
        username: str,
        password: str,
        tls: str = "false",
        get: int = 1,
        wallet_location: Optional[str] = None,
        oracle_home: Optional[str] = None,
        plugin_version: int = 1
        
    ):
        self.hostname = hostname
        self.port = port
        self.sid = sid
        self.username = username
        self.password = password
        self.use_tls = tls.lower() == "true"
        self.wallet_location = wallet_location
        self.plugin_version = plugin_version
        self.get = get
        self.cursor = None
        self.connection = None
        self.cache = QueryCache()

        self.metric_queries = {
            "Tablespace Queries": {
                "Tablespace Metrics Query": """
                SELECT 
                    t.tablespace_name,
                    t.total_size_mb,
                    NVL(f.free_space_mb, 0) as free_space_mb,
                    t.total_size_mb - NVL(f.free_space_mb, 0) as used_space_mb,
                    ROUND(100 - (NVL(f.free_space_mb, 0)/t.total_size_mb * 100), 2) as used_percent,
                    b.CONTENTS, 
                    b.LOGGING, 
                    b.STATUS 
                FROM (
                    SELECT tablespace_name, SUM(bytes)/1024/1024 as total_size_mb
                    FROM dba_data_files 
                    GROUP BY tablespace_name
                ) t
                LEFT JOIN (
                    SELECT tablespace_name, SUM(bytes)/1024/1024 as free_space_mb
                    FROM dba_free_space 
                    GROUP BY tablespace_name
                ) f ON t.tablespace_name = f.tablespace_name
                LEFT JOIN dba_tablespaces b ON t.tablespace_name = b.tablespace_name
                ORDER BY t.tablespace_name
                """,
                "Tablespace Datafile Query": """ SELECT FILE_NAME, (BYTES/1024/1024) , BLOCKS, AUTOEXTENSIBLE, (MAXBYTES/1024/1024), MAXBLOCKS, INCREMENT_BY, (USER_BYTES/1024/1024), USER_BLOCKS, TABLESPACE_NAME FROM DBA_DATA_FILES""",
            }
        }

    def connect(self) -> Tuple[bool, str]:
        """Establish connection to Oracle database"""
        try:
            import oracledb

            logger.info(
                "Connecting to Oracle: %s:%s/%s (TLS: %s)",
                self.hostname,
                self.port,
                self.sid,
                self.use_tls,
            )

            if self.use_tls:
                dsn = f"""(DESCRIPTION=
                        (ADDRESS=(PROTOCOL=tcps)(HOST={self.hostname})(PORT={self.port}))
                        (CONNECT_DATA=(SERVICE_NAME={self.sid}))
                        (SECURITY=(MY_WALLET_DIRECTORY={self.wallet_location}))
                        )"""
            else:
                dsn = f"{self.hostname}:{self.port}/{self.sid}"

            self.connection = oracledb.connect(
                user=self.username, password=self.password, dsn=dsn
            )
            self.cursor = self.connection.cursor()
            logger.info("Successfully connected to Oracle database")
            return True, "Connected"

        except Exception as e:
            error_msg = f"Connection failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def execute_query(self, query: str) -> List[Tuple]:
        """Execute SQL query and return results"""
        if not self.cursor:
            raise RuntimeError("Database connection not established")

        self.cursor.execute(query)
        results = list(self.cursor)
        logger.info("Query returned %d rows", len(results))
        return results

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

    def start(self) -> Dict:
        """Main entry point - returns metrics dict"""
        try:
            result = self.tablespace_complete()
            return result
        except Exception as e:
            logger.error("Error in start(): %s", e, exc_info=True)
            return {
                "status": 0,
                "msg": str(e),
                "plugin_version": plugin_version,
                "heartbeat_required": True,
            }

    def tablespace_complete(self) -> Dict:
        """Collect tablespace metrics using cache"""
        result = {
            "plugin_version": plugin_version,
            "heartbeat_required": True,
        }

        try:
            tbs_data, dfs_data = self.execute_tablespace_metrics()
            result["Tablespace_Details"] = tbs_data
            result["Tablespace_Datafile_Details"] = dfs_data
            result["Tablespaces monitored"] = str(len(tbs_data))
            result["Data files monitored"] = str(len(dfs_data)) + " files"

            logger.info(
                "Successfully collected %s tablespaces", result["Tablespaces monitored"]
            )
            logger.info(
                "Successfully collected %s datafiles", result["Data files monitored"]
            )

        except Exception as e:
            result["status"] = 0
            result["msg"] = str(e)
            logger.error("Error collecting tablespaces: %s", e, exc_info=True)

        return result

    def execute_tablespace_metrics(self) -> Tuple[List[Dict], List[Dict]]:
        """Execute tablespace query with caching"""
        tablespaces = None
        datafiles = None

        #  Step 1: Check if cache is valid
        if self.cache.is_cache_valid():
            logger.info("Using cached data")
            tablespaces = self.cache.read_cache("tablespace")
            datafiles = self.cache.read_cache("datafile")

        #  Step 2: If no valid cache, query DB (with locking)
        if tablespaces is None or datafiles is None:
            logger.info("Cache miss or expired, acquiring lock...")
            lock_fd = self.cache.acquire_lock(timeout=180)
            

            try:
                if lock_fd:
                    #  Step 3: Double-check cache (another process might have updated it)
                    if self.cache.is_cache_valid():
                        logger.info("Cache updated by another process")
                        tablespaces = self.cache.read_cache("tablespace")
                        datafiles = self.cache.read_cache("datafile")
                    else:
                        #  Step 4: Query database and update cache
                        logger.info("Querying database...")
                        connected, msg = self.connect()
                        if not connected:
                            raise RuntimeError(msg)

                        try:
                            tablespaces = self.execute_query(
                                self.metric_queries["Tablespace Queries"][
                                    "Tablespace Metrics Query"
                                ]
                            )
                            datafiles = self.execute_query(
                                self.metric_queries["Tablespace Queries"][
                                    "Tablespace Datafile Query"
                                ]
                            )

                            #  Step 5: Write to cache
                            self.cache.write_cache(tablespaces, "tablespace")
                            self.cache.write_cache(datafiles, "datafile")

                        finally:
                            self.close()
                else:
                    # Lock timeout handling
                    logger.warning("Lock timeout after 180s, waiting for cache...")
                    
                    for retry in range(10):
                        time.sleep(5)
                        if self.cache.is_cache_valid():
                            tablespaces = self.cache.read_cache("tablespace")
                            datafiles = self.cache.read_cache("datafile")
                            if tablespaces and datafiles:
                                logger.info("Cache populated (retry %d)", retry + 1)
                                break

            finally:
                #  Step 6: Always release lock
                if lock_fd:
                    self.cache.release_lock(lock_fd)

        #  Step 7: Process tablespaces for this page
        if tablespaces is None or datafiles is None:
            raise RuntimeError("Failed to get tablespace data")

        tbs_processor = TablespaceProcessor(tablespaces, int(self.get), "tablespace")
        tbs = tbs_processor.process_tablespaces()

        data_processor = TablespaceProcessor(datafiles, int(self.get), "datafile")
        # data_processor.to_dict_tbs = types.MethodType(to_dict_datafile,data_processor)
        dfs = data_processor.process_tablespaces()

        return tbs, dfs


class TablespaceProcessor:
    """Processes and paginates tablespace data"""

    def __init__(self, tablespaces: List[Tuple], page: int, process):
        if page < 1:
            raise ValueError(f"Page must be >= 1, got {page}")

        self.tablespaces = tablespaces
        self.page = page
        self.process = process
        self.page_size = 25
        self.page_start_idx = (self.page - 1) * self.page_size
        self.page_end_idx = self.page * self.page_size
        self.processed_tablespaces = []
        self.tablespace_names = []
        self.page_state = Pagination(page,process)
        self.page_state.load()
        self.requested_tablespaces = self.page_state.page()
        
        self.function_map = {
            "tablespace": self.to_dict_tbs,
            "datafile": self.to_dict_datafile
        }

        logger.info("Initialized processor for page %d", self.page)
        logger.info("Pagination range: [%d:%d]", self.page_start_idx, self.page_end_idx)
        logger.info("Requested tablespaces: %d", len(self.requested_tablespaces))

    def to_dict_tbs(
        self,
        name: str,
        total_size_mb: float,
        free_size_mb: float,
        used_space_mb: float,
        used_percent: float,
        contents: str,
        tbs_logging: str,
        status: str,
    ) -> Dict:
        """Convert tablespace row to dictionary format"""
        return {
            "name": name,
            "Tablespace_Size": round(total_size_mb, 2),
            "Tablespace_Free_Size": round(free_size_mb, 2),
            "Used_Space": round(used_space_mb, 2),
            "Used_Percent": round(used_percent, 2),
            "Contents": contents,
            "Logging": tbs_logging,
            "TB_Status": status,
            "status": 1 if status == "ONLINE" else 0,
        }

    def to_dict_datafile(
        self,
        name: str,
        data_file_size: float,
        data_file_blocks: float,
        autoextensible: str,
        max_data_file_size: float,
        max_data_file_blocks: float,
        increment_by: float,
        usable_data_file_size: float,
        usable_data_file_blocks: float,
        tbs_name: str
    ) -> Dict:
        """Convert tablespace row to dictionary format"""
        return {
            "name": name,
            "Data_File_Size": round(data_file_size, 2),
            "Data_File_Blocks": round(data_file_blocks, 2),
            "Autoextensible": autoextensible,
            "Max_Data_File_Size": round(max_data_file_size, 2),
            "Max_Data_File_Blocks": round(max_data_file_blocks),
            "Increment_By": round(increment_by),
            "Usable_Data_File_Size": round(usable_data_file_size),
            "Usable_Data_File_Blocks": round(usable_data_file_blocks),
            "Tablespace": tbs_name
        }

    def process_requested_tablespaces(self):
        """Process only explicitly requested tablespaces"""
        logger.info("Processing requested tablespaces")
        

        for row in self.tablespaces:
            tbs_name = row[0]
            if tbs_name in self.requested_tablespaces:
                if len(self.processed_tablespaces) >= self.page_size:
                    logger.warning("Page %d reached limit", self.page)
                    break
                self.processed_tablespaces.append(self.function_map[self.process](*row))
                self.tablespace_names.append(tbs_name)
                

        logger.info(
            "Processed %d requested %s", len(self.processed_tablespaces),self.process
            )
        logger.info(
            "Processed %s requested %s", self.tablespace_names,self.process
            )

    def paginate(self):
        """Paginate when the page is empty (first time setup)"""
        logger.info("Paginating page %d", self.page)
        logger.info("Paginating page %s", self.tablespaces)

        for row in self.tablespaces[self.page_start_idx : self.page_end_idx]:
            self.processed_tablespaces.append(self.function_map[self.process](*row))
            self.tablespace_names.append(row[0])

        logger.info("Paginated %d tablespaces", len(self.processed_tablespaces))

    def process_incomplete_page(self):
        """Process page with both requested and new tablespaces"""
        logger.info("Processing incomplete page")

        excluded_tablespace = self.page_state.get_excluded_tablespaces()

        for row in self.tablespaces:
            tbs_name = row[0]
            is_requested_in_page = tbs_name in self.requested_tablespaces
            included_in_page = tbs_name not in excluded_tablespace

            if is_requested_in_page or included_in_page:
                self.processed_tablespaces.append(self.function_map[self.process](*row))
                self.tablespace_names.append(tbs_name)

            if len(self.tablespace_names) >= 25:
                break

        logger.info("Processed %d tablespaces", len(self.processed_tablespaces))

    def deleted_tablespaces(self):
        """Mark deleted tablespaces (in JSON but not in DB) as offline"""
        not_available_tbs = set(self.requested_tablespaces).difference(
            self.tablespace_names
        )

        for tbs in not_available_tbs:
            self.processed_tablespaces.append({"name": tbs, "status": 0})
            logger.warning("Tablespace %s not found (marked offline)", tbs)

    def process_tablespaces(self) -> List[Dict]:
        """Process tablespace based on the page and page size"""
        logger.info("Starting processing for page %s", self.page)
        page_size = len(self.requested_tablespaces)

        if page_size >= 25:
            logger.info("Processing full page with 25 requested tablespaces")
            self.process_requested_tablespaces()
        elif page_size == 0:
            logger.info("Processing empty page (first time)")
            self.paginate()
            self.page_state.update(self.tablespace_names) # Update only if page is empty
        else:
            logger.info("Processing incomplete page with %d requested", page_size)
            self.process_incomplete_page()
            self.page_state.update(self.tablespace_names) # Update only if page is empty

        # Handle deleted tablespaces
        self.deleted_tablespaces()
        

        logger.info(
            "Returning %d tablespaces for page %d",
            len(self.processed_tablespaces),
            self.page,
        )
        return self.processed_tablespaces


class Pagination:
    """Manages pagination state (load/save JSON)"""

    def __init__(self, page_number: int, process: str):
        self.json_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            (os.path.basename(__file__) + "_{}.json".format(process)),
        )
        self.pagiation_state = {}
        self.page_number = str(page_number)

    def load(self) -> None:
        """Load pagination state from JSON file"""
        if os.path.isfile(self.json_path):
            try:
                with open(self.json_path, "r", encoding="utf-8") as file:
                    self.pagiation_state = json.load(file)
                logger.info(
                    "Loaded pagination state: %d pages", len(self.pagiation_state)
                )
            except Exception as e:
                logger.exception("Failed to load pagination state: %s", e)
                self.pagiation_state = {}
        else:
            logger.info("No existing pagination state found")
            self.pagiation_state = {}

    def update(self, tbs: List[str]) -> None:
        """Update tablespaces for the current page"""
        self.pagiation_state[self.page_number] = tbs
        logger.info(self.pagiation_state)

        try:
            with open(self.json_path, "w", encoding="utf-8") as file:
                json.dump(self.pagiation_state, file, indent=2)
            logger.info("Saved page %s with %d tablespaces", self.page_number, len(tbs))
        except Exception as e:
            logger.error("Failed to save pagination state: %s", e)

    def page(self) -> List[str]:
        """Get tablespaces for the current page"""
        return self.pagiation_state.get(self.page_number, [])

    def get_excluded_tablespaces(self) -> set:
        """Get all tablespaces from other pages as a set"""
        return set(
            chain.from_iterable(
                v for k, v in self.pagiation_state.items() if k != self.page_number
            )
        )


def main():
    """Main entry point"""

    defaults = {
        "hostname": "localhost",
        "port": "1521",
        "sid": "xe",
        "username": "USERNAME",
        "password": "PASSWORD",
        "tls": "False",
        "wallet_location": None,
        "oracle_home": "/opt/oracle/product/19c/dbhome_1/",
        "get": "1",
        "plugin_version": plugin_version
    }

    parser = argparse.ArgumentParser(description="Oracle Tablespace Monitoring Plugin")
    parser.add_argument(
        "--hostname", default=defaults["hostname"], help="Oracle database hostname"
    )
    parser.add_argument("--port", default=defaults["port"], help="Oracle database port")
    parser.add_argument("--sid", default=defaults["sid"], help="Oracle database SID")
    parser.add_argument(
        "--username", default=defaults["username"], help="Oracle database username"
    )
    parser.add_argument(
        "--password", default=defaults["password"], help="Oracle database password"
    )
    parser.add_argument(
        "--tls", default=defaults["tls"], help="Use TLS connection (True/False)"
    )
    parser.add_argument(
        "--wallet_location",
        default=defaults["wallet_location"],
        help="Oracle wallet location for TLS",
    )
    parser.add_argument(
        "--oracle_home",
        default=defaults["oracle_home"],
        help="Oracle home directory path",
    )
    parser.add_argument(
        "--get", default=defaults["get"], help="Page number to retrieve (1-based)"
    )
    parser.add_argument(
        "--plugin_version", default=defaults["plugin_version"], help="Plugin version"
    )

    args = parser.parse_args()
    logger.info("Starting Oracle Tablespace Monitor (page %s)", args.get)

    # Set Oracle home environment variable
    if args.oracle_home:
        os.environ["ORACLE_HOME"] = args.oracle_home

    # Validate page number
    if int(args.get) > 0:
        monitor = OracleMonitor(**vars(args))
        result = monitor.start()
    else:
        result = {
            "status": 0,
            "msg": "Enter a Valid get value. Get value should be greater than 0",
            "plugin_version": plugin_version,
            "heartbeat_required": True,
        }

    # Output JSON result
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
