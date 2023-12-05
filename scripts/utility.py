def get_daily_logs(all_logs):
  print(all_logs)
  summarized_log_list = []
  for log in all_logs:
    log_object = {
      "date": log.date,
      "distance": log.distance,
      "duration": log.time,
    }
    print(log_object)
    if len(summarized_log_list) == 0:
      summarized_log_list.append(log_object)
    else:
      date_found = False
      for summarized_log in summarized_log_list:
        if summarized_log["date"] == log_object["date"]:
          summarized_log["distance"] = summarized_log["distance"] + log_object["distance"]
          summarized_log["duration"] = summarized_log["duration"] + log_object["duration"]
          date_found = True
      if not date_found:
        summarized_log_list.append(log_object)
  sorted_by_date = sorted(summarized_log_list, key=lambda x: x["date"], reverse=True)

  with_avarage_speed = [{"date": log["date"], "distance":log["distance"], "duration": log["duration"], "speed": round(60/log["duration"] * log["distance"], 2)} for log in sorted_by_date]
  print(with_avarage_speed)

  return with_avarage_speed[:10]

def sort_logs_by_date(all_logs):
  print(all_logs)