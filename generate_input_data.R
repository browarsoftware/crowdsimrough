# ORDER OF RUN: #2
# Set path to data, run for each csv separately

# Change files to 90, 100, 120, 140, 160, 180, 200 
df = read.csv('D:\\Projects\\Python\\PycharmProjects\\tf28\\symulacja_tlumu\\gotowe\\NA_GITHUB\\data\\results_to_file_b200.txt', sep=";")
out_file = 'D:\\Projects\\Python\\PycharmProjects\\tf28\\symulacja_tlumu\\gotowe\\NA_GITHUB\\data\\results_to_file_imp_b200.txt'
out_file_no_zero = 'D:\\Projects\\Python\\PycharmProjects\\tf28\\symulacja_tlumu\\gotowe\\NA_GITHUB\\data\\results_to_file_imp_no_zero_b200.txt'


t_xy_n = sqrt(df$t_x ^ 2 + df$t_y ^ 2)
df$t_xn = df$t_x
df$t_yn = df$t_y
for (a in 1:length(df$t_xn))
{
  if (t_xy_n[a] > 0)
  {
    df$t_xn[a] = df$t_xn[a] / t_xy_n[a]
    df$t_yn[a] = df$t_yn[a] / t_xy_n[a]
  }
}


cd = function(x,y) {
  xr = round(x)
  yr = round(y)
  res = 0
  if (xr == 0 && yr == 0)
    res = 0
  if (xr == 1 && yr == 0)
    res = 1
  if (xr == 1 && yr == 1)
    res = 2
  if (xr == 0 && yr == 1)
    res = 3
  if (xr == -1 && yr == 1)
    res = 4
  if (xr == -1 && yr == 0)
    res = 5
  if (xr == -1 && yr == -1)
    res = 6
  if (xr == 0 && yr == -1)
    res = 7
  if (xr == 1 && yr == -1)
    res = 8

  return (res)
}


df$t_dir = rep(0, length(df$key))
for (a in 1:length(df$t_dir))
{
  df$t_dir[a] = cd(df$t_xn[a], df$t_yn[a])
}

df$ff_dir = rep(0, length(df$key))
for (a in 1:length(df$t_dir))
{
  df$ff_dir[a] = cd(df$ff_x[a], df$ff_y[a])
}

df_no_Zero = df[df$t_dir != 0,]

write.csv(df_no_Zero, out_file_no_zero, sep=";",quote = FALSE, row.names = FALSE)
write.csv(df, out_file, sep=";",quote = FALSE, row.names = FALSE)

