#!/usr/bin/python3
import time
from re import search
import json
import os
import datetime
import requests
import argparse
import traceback

from slack import WebClient
from slack.errors import SlackApiError

CHANNEL_NAME = ""
CHANNEL_TYPE = ""

data = {}
data["plugin_version"] = "1"
data["heartbeat_required"] = "true"

auth_token = ""

parser = argparse.ArgumentParser()
parser.add_argument('--oauth_token')
parser.add_argument('--channel_name')
parser.add_argument('--channel_type')
args = parser.parse_args()
if args.oauth_token:
    auth_token = str(args.oauth_token)
if args.channel_name:
    CHANNEL_NAME = str(args.channel_name)
if args.channel_type:
    CHANNEL_TYPE = str(args.channel_type)

headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

############################################ CHANNEL TYPES ######################################################
PUBLIC_CHANNEL_TYPE = "public_channel"
PRIVATE_CHANNEL_TYPE = "private_channel"
DIRECT_MESSAGE_CHANNEL_TYPE = "direct_message"
MULTI_PARTY_DIRECT_MESSAGE_CHANNEL_TYPE = "multi_party_direct_message"
################################################################################################################################################################################

invalid_channel_name_or_channel_type = "Invalid Channel Name or Channel Type. Please Enter the Correct Channel name and Channel Type"
video_extentions = "webm_SEPA_mkv_SEPA_flv_SEPA_vob_SEPA_ogv_SEPA_ogg_SEPA_drc_SEPA_gif_SEPA_gifv_SEPA_mng_SEPA_avi_SEPA_mts_SEPA_m2ts_SEPA_ts_SEPA_mov_SEPA_qt_SEPA_wmv_SEPA_yuv_SEPA_rm_SEPA_rmvb_SEPA_asf_SEPA_amv_SEPA_mp4_SEPA_m4p_SEPA_m4v_SEPA_mpg_SEPA_mp2_SEPA_mpeg_SEPA_mpe_SEPA_mpv_SEPA_m2v_SEPA_svi_SEPA_3gp_SEPA_mxf_SEPA_roq_SEPA_nsv_SEPA_f4v_SEPA_f4p_SEPA_f4a_SEPA_f4b_SEPA_m4r_SEPA_hdv_SEPA_oga_SEPA_ogx_SEPA_wma_SEPA_m4b_SEPA_3gp2_SEPA_3g2_SEPA_3gpp_SEPA_3gpp2_SEPA_asf"
audio_extentions = "8svx_SEPA_aac_SEPA_ac3_SEPA_aiff_SEPA_amb_SEPA_au_SEPA_avr_SEPA_caf_SEPA_cdda_SEPA_cvs_SEPA_cvsd_SEPA_cvu_SEPA_dts_SEPA_dvms_SEPA_fap_SEPA_flac_SEPA_fssd_SEPA_gsrt_SEPA_hcom_SEPA_htk_SEPA_ima_SEPA_ircam_SEPA_m4a_SEPA_m4r_SEPA_maud_SEPA_mp2_SEPA_mp3_SEPA_nist_SEPA_ogs_SEPA_ogg_SEPA_opus_SEPA_paf_SEPA_prc_SEPA_pvf_SEPA_ra_SEPA_sd2_SEPA_sln_SEPA_smp_SEPA_snd_SEPA_sndr_SEPA_sndt_SEPA_sou_SEPA_sph_SEPA_spx_SEPA_tta_SEPA_txw_SEPA_vms_SEPA_voc_SEPA_vox_SEPA_w64_SEPA_wav_SEPA_wma_SEPA_wv_SEPA_wve_SEPA_3ga_SEPA_aa_SEPA_aa3_SEPA_aac_SEPA_aaif_SEPA_alac_SEPA_amr_SEPA_ape_SEPA_awb_SEPA_dct_SEPA_dss_SEPA_dvf_SEPA_gsm_SEPA_iklax_SEPA_ivs_SEPA_mpc_SEPA_msv_SEPA_nmf_SEPA_nsf_SEPA_mogg_SEPA_opus_SEPA_ra_SEPA_rm_SEPA_raw_SEPA_rf64_SEPA_tta_SEPA_wv_SEPA_wma_SEPA_webm_SEPA_cda"
image_extentions = "tif_SEPA_jpg_SEPA_png_SEPA_jpeg_SEPA_tiff_SEPA_bmp_SEPA_eps_SEPA_raw_SEPA_cr2_SEPA_nef_SEPA_orf_SEPA_sr2"
executable_file_extentions = "oxe_SEPA_agp_SEPA_action_SEPA_app_SEPA_applescript_SEPA_bat_SEPA_cgi_SEPA_cod_SEPA_com_SEPA_dek_SEPA_dex_SEPA_ebm_SEPA_elf_SEPA_es_SEPA_esh_SEPA_ex4_SEPA_exe_SEPA_exopc_SEPA_fpi_SEPA_gpe_SEPA_gpu_SEPA_hms_SEPA_hta_SEPA_ipa_SEPA_isu_SEPA_jar_SEPA_jsx_SEPA_kix_SEPA_mau_SEPA_mel_SEPA_mem_SEPA_mrc_SEPA_pex_SEPA_pef_SEPA_plsc_SEPA_prg_SEPA_ps1_SEPA_pwc_SEPA_qit_SEPA_rbx_SEPA_rox_SEPA_rxe_SEPA_scar_SEPA_scb_SEPA_scpt_SEPA_sct_SEPA_seed_SEPA_u3p_SEPA_vb_SEPA_vbe_SEPA_vbs_SEPA_vbscript_SEPA_vlx_SEPA_widget_SEPA_workflow_SEPA_ws_SEPA_xbe_SEPA_xex_SEPA_xys_SEPA_java_SEPA_jsp_SEPA_py_SEPA_xpi_SEPA_htm_SEPA_html_SEPA_sh_SEPA_css_SEPA_xhtml_SEPA_jhtml_SEPA_jspx_SEPA_wss_SEPA_yaws_SEPA_swf_SEPA_asp_SEPA_php_SEPA_php4_SEPA_php3_SEPA_rb_SEPA_rhtml_SEPA_shtml_SEPA_xml_SEPA_rss_SEPA_svg_SEPA_cgi_SEPA_dll_SEPA_json"

PUBLIC_CHANNELS_API = "https://slack.com/api/users.conversations?" + "&types=public_channel"
PRIVATE_CHANNELS_API = "https://slack.com/api/users.conversations?" + "&types=private_channel"
DIRECT_MESSAGE_API = "https://slack.com/api/conversations.list?" + "&types=im"
MULTI_PARTY_DIRECT_MESSAGE_API = "https://slack.com/api/conversations.list?" + "&types=mpim"
STARS_API = "https://slack.com/api/stars.list?" + "&limit=999"


def get_initial_file_read_api(channel_id):
    INITIAL_FILE_READ_API = "https://slack.com/api/files.list?" + "&channel=" + channel_id + "&count=1000"
    return INITIAL_FILE_READ_API


def get_time_based_file_read_api(channel_id):
    TIME_BASED_FILE_READ_API = "https://slack.com/api/files.list?" + "&channel=" + channel_id + "&ts_from=" + previous_timestamp + "&ts_to=" + str(datetime.datetime.now().timestamp())
    return TIME_BASED_FILE_READ_API


def get_initial_message_count_api(channel_id):
    INITIAL_MESSAGE_COUNT_API = "https://slack.com/api/conversations.history?" + "&channel=" + channel_id + "&limit=1000"
    return INITIAL_MESSAGE_COUNT_API


def get_time_based_message_count_api(channel_id):
    TIME_BASED_MESSAGE_COUNT_API = "https://slack.com/api/conversations.history?" + "&channel=" + channel_id + "&limit=1000" + "&oldest=" + previous_timestamp
    return TIME_BASED_MESSAGE_COUNT_API


def get_scheduled_message_count_api(channel_id):
    SCHEDULED_MESSAGES_API = "https://slack.com/api/chat.scheduledMessages.list?" + "&channel=" + channel_id + "&limit=999"
    return SCHEDULED_MESSAGES_API


def get_pin_count_api(channel_id):
    PIN_COUNT_API = "https://slack.com/api/pins.list?" + "&channel=" + channel_id
    return PIN_COUNT_API


METRIC_UNITS = {
	"total_files" : "count",
	"total_users" : "count",
    "public_channels" : "count",
    "user_groups" : "count",
    "total_file_sizes" : "count",
    "remainder_count" : "count"
}
data["units"] = METRIC_UNITS
count_stats = {}
COUNT_STATS_FILE = "./channel_count_stat.txt"
previous_private_channels_message_count = ""
previous_public_channels_message_count = ""
previous_direct_message_count = ""
previous_multi_party_channels_message_count = ""
previous_files_count = ""
previous_timestamp = ""
previous_total_file_size = ""
previous_video_files = ""
previous_audio_files = ""
previous_image_files = ""
previous_executable_files = ""
previous_other_files = ""


pin_count = 0
scheduled_messages_count = 0
files_list = {}
members_list = {}
client = {}
channel_id = ""

def request_falied(response):
    if "error" in response.keys():
        data["status"] = 0
        data["msg"] = str(response["error"])
        print(json.dumps(data))
        exit()
    else:   
        return
    

def initialize_WebClient():
    global client
    global auth_token
    try:
         client = WebClient(auth_token)
    except Exception as config_error:
        construct_error_message(str(config_error))


def load_previous_data_from_count_stat_file():
    global previous_public_channels_message_count
    global previous_private_channels_message_count
    global previous_files_count
    global previous_multi_party_channels_message_count
    global previous_direct_message_count
    global previous_timestamp
    global previous_total_file_size
    global previous_video_files
    global previous_audio_files
    global previous_image_files
    global previous_executable_files
    global previous_other_files
    if os.path.isfile(COUNT_STATS_FILE):
        with open(COUNT_STATS_FILE) as json_file:
            json_data = json.load(json_file)
            if CHANNEL_TYPE == PUBLIC_CHANNEL_TYPE:
                previous_public_channels_message_count = str(json_data["public_channels_message_count"])
            elif CHANNEL_TYPE == PRIVATE_CHANNEL_TYPE:
                previous_private_channels_message_count = str(json_data["private_channels_message_count"])
            elif CHANNEL_TYPE == DIRECT_MESSAGE_CHANNEL_TYPE:
                previous_direct_message_count = str(json_data["direct_message_count"])
            elif CHANNEL_TYPE == MULTI_PARTY_DIRECT_MESSAGE_CHANNEL_TYPE:
                previous_multi_party_channels_message_count = str(json_data["multi_party_channels_message_count"])

            previous_timestamp = str(json_data["Last_updated_timestamp"])
            previous_files_count = str(json_data["total_files"])
            previous_total_file_size = str(json_data["total_file_size"])
            previous_video_files = str(json_data["video_files"])
            previous_audio_files = str(json_data["audio_files"])
            previous_image_files = str(json_data["image_files"])
            previous_executable_files = str(json_data["executable_files"])
            previous_other_files = str(json_data["other_files"])



def load_file_info():
    global files_list
    file_url = ""
    try:

        if not os.path.isfile(COUNT_STATS_FILE):
             file_url = get_initial_file_read_api(channel_id)
        else:
             file_url = get_time_based_file_read_api(channel_id)
        file_response = requests.get(file_url,headers=headers)
        files_list = json.loads(file_response.text)
        request_falied(files_list)
    except SystemExit:
        exit()
    except Exception:
        construct_error_message(str(files_list))


def get_total_files():
    global files_list
    try:
        files_count = len(files_list["files"])
        if len(previous_files_count) > 0:
            files_count = files_count + int(previous_files_count)
        data["total_files"] = str(files_count)
        count_stats["total_files"] = str(files_count)
    except Exception as total_files_error:
        construct_error_message(total_files_error)


def total_members_list():
    global  members_list
    try:
        members_list = client.users_list()
        data["total_users"] =  str((len(members_list["members"]))-2)
    except Exception as e:
        construct_error_message(str(e))



def get_scheduled_messages_count():
    scheduled_messages = {}
    try:
        scheduled_response = requests.get(get_scheduled_message_count_api(channel_id),headers=headers)
        scheduled_messages = json.loads(scheduled_response.text)
        request_falied(scheduled_messages)
        return len(scheduled_messages["scheduled_messages"])
    except Exception as e:
        construct_error_message(str(e))


def remainder_list():
    remainder = {}
    try:
        remainder = client.reminders_list()
        data["remainder_count"] = str(len(remainder["reminders"]))
    except Exception as e:
        construct_error_message(str(e))


def stars_list():
    stars_list = {}
    try:
        stars_response = requests.get(STARS_API,headers=headers)
        stars_list = json.loads(stars_response.text)
        request_falied(stars_list)
        data["is_stared"] = "False"
        for stars_info in stars_list["items"]:
            if str(stars_info["channel"]) == channel_id:
                data["is_stared"] = "True"

    except Exception as e:
        construct_error_message(str(e))


def get_reaction_list(userid):
    reaction_list = {}
    try:
        reaction_response = requests.get("https://slack.com/api/reactions.list?" + "&full=true&limit=1000",headers=headers)
        reaction_list = json.loads(reaction_response.text)
        request_falied(reaction_list)
        return len(reaction_list["items"])
    except Exception as e:
        construct_error_message(str(e))


def get_dnd_info():
    do_not_disturb = {}
    try:
        do_not_disturb = client.dnd_info()
        data["do_not_distrub_enabled"] = str(do_not_disturb["dnd_enabled"])
        start_time = get_date_time(do_not_disturb["next_dnd_start_ts"])
        end_time = get_date_time(do_not_disturb["next_dnd_end_ts"])
        time_range = str(start_time) + " - " + str(end_time)
        data["next_do_not_distrub_start_and_end_time"] = time_range
        data["do_not_disturb_snooze_enabled"] = str(do_not_disturb["snooze_enabled"])
    except Exception as e:
        construct_error_message(str(e))



def get_date_time(UnixTime):
    date_time = datetime.datetime.fromtimestamp(
        int(UnixTime)
    ).strftime('%Y-%m-%d %H:%M:%S')
    return date_time



def get_total_files_info():
    global  files_list
    size = 0
    videos_files = 0
    images_files = 0
    audios_files = 0
    executable_files = 0
    other_files = 0
    try:
                for file in files_list["files"]:
                    size = size + file["size"]
                    fileName = str(file["name"])
                    extention = os.path.splitext(fileName)[1][1:].strip().lower()
                    mimetype = str(file['mimetype'])
                    if (search("video",mimetype)) or ((not(search("audio",mimetype))) and (search(extention, video_extentions))):#some of the extention remains same in audio and videos..so we use this condition not(search("audio",mimetype)
                        videos_files = videos_files + 1
                    elif (search("image",mimetype)) or (search(extention,image_extentions)):
                        images_files = images_files + 1
                    elif (search("audio",mimetype)) or (search(extention,audio_extentions)):
                        audios_files = audios_files + 1
                    elif (search("text",mimetype)) or (search(extention,executable_file_extentions)):
                        executable_files = executable_files + 1
                    else:
                        other_files = other_files + 1
                file_sizes = int((size / (1024 * 1024)))
                isFile = os.path.isfile(COUNT_STATS_FILE)
                if isFile:
                    file_sizes = file_sizes + int(previous_total_file_size)
                if file_sizes > 0 or size != 0:
                    data["total_file_size"] = str(file_sizes)
                    count_stats["total_file_size"] = str(file_sizes)
                else:
                    data["total_file_size"] = str(size)
                    count_stats["total_file_size"] = str(size)


                if isFile:
                    videos_files = videos_files + int(previous_video_files)
                    audios_files = audios_files + int(previous_audio_files)
                    images_files = images_files + int(previous_image_files)
                    executable_files = executable_files + int(previous_executable_files)
                    other_files = other_files + int(previous_other_files)

                data["video_files"] = str(videos_files)
                count_stats["video_files"] = str(videos_files)
                data["audio_files"] = str(audios_files)
                count_stats["audio_files"] = str(audios_files)
                data["image_files"] = str(images_files)
                count_stats["image_files"] = str(images_files)
                data["executable_files"] = str(executable_files)
                count_stats["executable_files"] = str(executable_files)
                data["other_files"] = str(other_files)
                count_stats["other_files"] = str(other_files)

    except Exception as e:
        construct_error_message(str(e))


def get_public_channels_list():
    public_channels_list = {}
    global  channel_id
    try:
        public_channels_response = requests.get(PUBLIC_CHANNELS_API,headers=headers)
        public_channels_list = json.loads(public_channels_response.text)
        request_falied(public_channels_list)
        data["public_channels_count"] = str(len(public_channels_list["channels"]))


        for public_info in public_channels_list["channels"]:
            if str(public_info["name"]) == CHANNEL_NAME:
                channel_id = str(public_info["id"])
                public_message_count = get_message_count(str(public_info["id"]))
                if len(previous_public_channels_message_count) > 0:
                    public_message_count = public_message_count + int(previous_public_channels_message_count)
                data[CHANNEL_NAME+"_message_count"] = str(public_message_count)
                count_stats["public_channels_message_count"] = str(public_message_count)
                return
        construct_error_message(invalid_channel_name_or_channel_type)
    except Exception as e:
        construct_error_message(str(e))


def get_private_channels_list():
    private_channels_list = {}
    global  channel_id
    try:
        private_channels_response = requests.get(PRIVATE_CHANNELS_API,headers=headers)
        private_channels_list = json.loads(private_channels_response.text)
        request_falied(private_channels_list)
        data["private_channels_count"] = str(len(private_channels_list["channels"]))
        for private_info in private_channels_list["channels"]:
            if str(private_info["name"] == CHANNEL_NAME):
                 channel_id = str(private_info["id"])
                 private_message_count = get_message_count(str(private_info["id"]))
                 if len(previous_private_channels_message_count) > 0:
                    private_message_count = private_message_count + int(previous_private_channels_message_count)
                 data[CHANNEL_NAME+"_message_count"] = str(private_message_count)
                 count_stats["private_channels_message_count"] = str(private_message_count)
                 return
        construct_error_message(invalid_channel_name_or_channel_type)
    except Exception as e:
        construct_error_message(str(e))

def get_message_count(id):
    global pin_count
    global scheduled_messages_count
    message_list = {}
    url = ""
    #constants = Constants(id,previous_timestamp)
    try:
        if not os.path.isfile(COUNT_STATS_FILE):
            url = url + get_initial_message_count_api(id)
        else:
            url = url + get_time_based_message_count_api(id)

        message_response = requests.get(url,headers=headers)
        message_list = json.loads(message_response.text)
        request_falied(message_list)

        if CHANNEL_TYPE != DIRECT_MESSAGE_CHANNEL_TYPE:
            pin_count = pin_count + int(message_list["pin_count"])
        else:
            pin_count = pin_count + get_pin_count()
        scheduled_messages_count = scheduled_messages_count + get_scheduled_messages_count()
        return len(message_list["messages"])
    except Exception as e:
        construct_error_message(str(e))


def get_direct_message_channels_list():
    direct_message_channels_list = {}
    global members_list
    global channel_id
    try:
        direct_message_channels_response = requests.get(DIRECT_MESSAGE_API,headers=headers)
        direct_message_channels_list = json.loads(direct_message_channels_response.text)
        request_falied(direct_message_channels_list)
        user_id = ""

        for user_info in members_list["members"]:
            if str(user_info["name"]) == CHANNEL_NAME:
                user_id = str(user_info["id"])
                break

        for direct_message_info in direct_message_channels_list["channels"]:
            if str(direct_message_info["user"]) == user_id:
                channel_id = str(direct_message_info["id"])
                direct_message_count = get_message_count(str(direct_message_info["id"]))
                if len(previous_direct_message_count) > 0:
                    direct_message_count = direct_message_count + int(previous_direct_message_count)
                data[CHANNEL_NAME+"_direct_message_count"] = str(direct_message_count)
                count_stats["direct_message_count"] = str(direct_message_count)
                return
        construct_error_message(invalid_channel_name_or_channel_type)
    except Exception as e:
        construct_error_message(str(e))


def get_multi_party_direct_message_channels_list():
    multi_part_channels_list = {}
    global  channel_id
    try:
        multi_party_channels_response = requests.get(MULTI_PARTY_DIRECT_MESSAGE_API,headers=headers)
        multi_part_channels_list = json.loads(multi_party_channels_response.text)
        request_falied(multi_part_channels_list)
        data["multi_party_channels_count"] = str(len(multi_part_channels_list["channels"]))
        for multi_party_info in multi_part_channels_list["channels"]:
            if str(multi_party_info["name"]) == CHANNEL_NAME:
                channel_id = str(multi_party_info["id"])
                multi_party_message_count = get_message_count(str(multi_party_info["id"]))
                if len(previous_multi_party_channels_message_count) > 0:
                    multi_party_message_count = multi_party_message_count + int(previous_multi_party_channels_message_count)
                data[CHANNEL_NAME+"_message_count"] = str(multi_party_message_count)
                count_stats["multi_party_channels_message_count"] = str(multi_party_message_count)
                return
        construct_error_message(invalid_channel_name_or_channel_type)
    except Exception as e:
        construct_error_message(str(e))


def get_current_timestamp():
    return str(datetime.datetime.now().timestamp())


def load_count_stat_in_file():
    try:
      count_stats["Last_updated_timestamp"] = get_current_timestamp()
      with open(COUNT_STATS_FILE,'w') as stats_file:
          json.dump(count_stats,stats_file)
    except Exception as file_write_error:
        construct_error_message(file_write_error)

def get_pin_count():
    pin_list = {}
    try:
        pin_response = requests.get(get_pin_count_api(channel_id),headers=headers)
        pin_list = json.loads(pin_response.text)
        request_falied(pin_list)
        return len(pin_list["items"])
    except Exception as e:
        construct_error_message(str(e))

def construct_error_message(error):
    data["status"] = 0
    data["msg"] = error
    #traceback.print_exc()
    print(json.dumps(data))
    exit()


if __name__ == "__main__":
 initialize_WebClient()
 load_previous_data_from_count_stat_file()
 total_members_list()
 if CHANNEL_TYPE == PUBLIC_CHANNEL_TYPE:
    get_public_channels_list()
 elif CHANNEL_TYPE == PRIVATE_CHANNEL_TYPE:
    get_private_channels_list()
 elif CHANNEL_TYPE == DIRECT_MESSAGE_CHANNEL_TYPE:
     
     get_direct_message_channels_list()
 elif CHANNEL_TYPE == MULTI_PARTY_DIRECT_MESSAGE_CHANNEL_TYPE:
     get_multi_party_direct_message_channels_list()
 load_file_info()
 get_total_files()
 get_total_files_info()
 remainder_list()
 stars_list()
 get_dnd_info()
 load_count_stat_in_file()
 data["pin_count"] = str(pin_count)
 data["scheduled_messages_count"] = str(scheduled_messages_count)
 print(json.dumps(data, indent=4, sort_keys=True))
