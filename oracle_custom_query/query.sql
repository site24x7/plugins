SELECT VALUE, NAME FROM gv$pgastat where NAME IN ('total PGA allocated', 'total freeable PGA memory', 'maximum PGA allocated','total PGA inuse')
