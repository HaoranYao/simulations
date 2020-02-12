
import csv
class Collector(object):
    def __init__(self, args):
        self.model = args.model
        self.connection_target = args.connection_target
        self.endtime = args.end_time
        self.server_number = args.server_number
        self.bucket_number = args.bucket_number
        self.temp_count, self.total_count,self.change_time = 0, 0, 0
        self.total_con = 0

    def conclusion(self):
        pass

class StatisticsCollector(Collector):
    def __init__(self, args):
        super(StatisticsCollector, self).__init__(args)
        self.max_imba = 0
        self.ave_imba = 0

    def conclusion(self):
        self.change_time += 1
        with open("./stats/report.csv",'ab+') as f:
            aa = csv.writer(f)
            aa.writerow([str(self.model), str(self.connection_target), str(self.endtime), str(self.server_number), "None",
                         str(self.bucket_number),"None", "None", "None", "None", "None", str(self.ave_imba * 100), "None"])
            f.close()

class DynamicBeamerCollecter(Collector):
    def __init__(self, args):
        super(DynamicBeamerCollecter, self).__init__(args)
        self.unnecessary_move_count = 0
        self.current_connection = 0
        self.Imbalance_threshold = args.Imbalance_threshold
        self.moving_number = 0
        self.moving_bucket = 0.0

    def conclusion(self):
        with open("./stats/report.csv", 'ab+') as f:
            aa = csv.writer(f)
            aa.writerow([str(self.model), str(self.connection_target), str(self.endtime), str(self.server_number), "None",
                         str(self.bucket_number), str((self.Imbalance_threshold-1)*100), str(self.total_con), str(self.unnecessary_move_count),
                         str((float(self.unnecessary_move_count) / self.total_con)*100), "None", "None", str((self.moving_bucket/float(self.bucket_number))*100)])
            f.close()
        self.moving_bucket = 0.0

class DipCollector(Collector):
    def __init__(self, args):
        super(DipCollector, self).__init__(args)
        self.unnecessary_move_count = 0
        self.rate_number = args.update_rate
        self.current_connection = 0


    def conclusion(self):
        self.change_time += 1
        if self.change_time == 30000:
            self.change_time = 0
            print (str(float(self.unnecessary_move_count)/self.total_con))
            with open("./stats/report.csv",'ab+') as f:
                aa = csv.writer(f)
                aa.writerow([str(self.model), str(self.connection_target), str(self.endtime), str(self.server_number),
                             str(self.rate_number),"None", "None", str(self.total_con),str(self.unnecessary_move_count),str((float(self.unnecessary_move_count)/self.total_con)*100), "None", "None", "None"])
                f.close()
