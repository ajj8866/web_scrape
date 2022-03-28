       # id_ls, uuid_ls, date_ls, tte_ls, ctry_ls, ev_ls, imp_ls, prev_ls, cons_ls, act_ls, tm_ls = [], [],[], [], [], [], [], [], [], [], []
        # for i in range(len(self.df)):
        #     id_ls.append(self.df['ID'].iloc[i])
        #     uuid_ls.append(str(self.df['UUID'].iloc[i]))
        #     date_ls.append(self.df['Date'].iloc[i])
        #     tte_ls.append(self.df['Time to Event'].iloc[i])
        #     ctry_ls.append(self.df['Country'].iloc[i])
        #     ev_ls.append(self.df['Event'].iloc[i])
        #     imp_ls.append(self.df['Impact'].iloc[i])
        #     prev_ls.append(self.df['Previous'].iloc[i])
        #     cons_ls.append(self.df['Consensus'].iloc[i])
        #     act_ls.append(self.df['Actual'].iloc[i])
        #     #tm_ls.append(self.df['Formatted Date'].iloc[i])
        #self.data_dict = {'ID': id_ls, 'UUID': uuid_ls, 'Date': date_ls, 'Time to Event': tte_ls, 'Country': ctry_ls, 'Event': ev_ls, 'Impact': imp_ls, 'Previous': prev_ls, 'Consensus': cons_ls, 'Actual': act_ls} #, 'Formatted Date': tm_ls}

        #     def calData(self):
        # json_cal = Path(Path.cwd(), 'Datapipe', 'raw_data', 'news_data.json')
        # print(json_cal.exists)
        # if json_cal.is_file() == False:
        #     with open(json_cal, 'w') as fw:
        #         json.dump(self.data_dict, fw)
        # else:
        #     with open(json_cal, 'r+') as f:
        #         try:
        #             pyfile = json.load(f)
        #             f.seek(0)
        #             for id, uuid, dte, ttevent, ctry, ev, imp, pre, con, act  in zip(self.data_dict['ID'], self.data_dict['UUID'], self.data_dict['Date'], self.data_dict['Time to Event'], self.data_dict['Country'], self.data_dict['Event'], self.data_dict['Impact'], self.data_dict['Previous'], self.data_dict['Consensus'], self.data_dict['Actual']): #, self.data_dict['Formatted Date']):
        #                 #formd
        #                 if id not in pyfile['ID']:
        #                     pyfile['ID'].append(id)
        #                     pyfile['UUID'].append(uuid)
        #                     pyfile['Date'].append(dte)
        #                     pyfile['Time to Event'].append(ttevent)
        #                     pyfile['Country'].append(ctry)
        #                     pyfile['Event'].append(ev)
        #                     pyfile['Impact'].append(imp)
        #                     pyfile['Previous'].append(pre)
        #                     pyfile['Consensus'].append(con)
        #                     pyfile['Actual'].append(act)
        #                     #pyfile['Formatted Date'].append(formd)
        #             f.seek(0)
        #             json.dump(pyfile, f)
        #             print(pyfile)
        #         except Exception as e:
        #             print('Exception')
        #             print(e)
        #             print('yeah excep')
        #             f.seek(0)
        #             json.dump(self.data_dict, f)
        #     f.close()
