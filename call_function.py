import function

function.down_load() #下載股票資料原始檔
function.read_lastest_data() #從最後一筆讀取csv檔
function.con_save_mov_avg() #5/20/60日均值計算並寫入到mov.csv
#function.insert_prev_mov_avg() #插補5/20/60日前一日均值並寫入到mov.csv
#function.analysis_avg_up() #篩選出5日均值向上穿過20日均值並寫入到up.csv
#function.analysis_avg_down() #篩選出5日均值向下穿過20日均值並寫入到down.csv