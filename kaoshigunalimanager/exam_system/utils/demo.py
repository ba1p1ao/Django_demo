# import pymysql
# import time

# # 创建数据库连接
# db = pymysql.connect(
#     host="localhost",  # 数据库主机地址
#     user="root",  # 用户名
#     password="123",  # 密码
#     database="exam_system"  # 数据库名称
# )

# # 创建游标对象
# cursor = db.cursor()

# # 执行 SQL 查询
# cursor.execute("select * from question")
# desc = cursor.description
# alldata = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
# # print(alldata)


# # 修改 以ABCD的方式返回
# # for data in alldata:
# #     if data["options"] and "[" == data["options"][0] and "]" == data["options"][-1]:
# #         newoptions = data["options"]
# #         ops = newoptions[1:-1].split(", ")
# #         print(data['answer'])
# #         newanswer = data['answer']
# #         ans = data['answer'].split(",")
# #         newanswerlist = []
# #         for i, op in enumerate(ops):
# #             # print(op, end="")
# #
# #             for a in ans:
# #                 if op[1:-1] == a:
# #                     newanswerlist.append(chr(i+ord('A')))
# #                     break
# #         print(newanswerlist)
# #         # newstr = f'"A": {ops[0]}, "B": {ops[1]}, "C": {ops[2]}, "D": {ops[3]}'
# #         newoptionsstr = '{"A": %s, "B": %s, "C": %s, "D": %s}' % (ops[0], ops[1], ops[2], ops[3])
# #         newanswerstr = newanswerlist.__str__().replace("'", '"')
# #         print(newoptionsstr, newanswerstr)

#         # update_sql = f"update question set options = '{newoptionsstr}', answer = '{newanswerstr}' where id = {data['id']}"
#         #
#         # # 执行SQL语句
#         # cursor.execute(update_sql)
#         # # 提交到数据库执行
#         # db.commit()

# # 修改answer 列表长度为1的时候直接返回字符

# for data in alldata:
#     if data["type"] in ["multiple"]:
#         # if "," not in data["answer"] and '"' in data["answer"]:
#         if '"' in data["answer"]:
#             print(data["content"])
#             print(data["answer"])
#             new_answer = data["answer"].replace('"', '').replace('[', '').replace(']', '')
#             print(new_answer)
#             update_sql = f"update question set answer = '{new_answer}' where id = {data['id']}"
#             # print(update_sql)
#             # 执行SQL语句
#             cursor.execute(update_sql)
#             # 提交到数据库执行
#             db.commit()
# # 关闭连接
# db.close()


# # from datetime import datetime

# # s = "2000-12-30 10:20:02"
# # t = "%Y-%m-%d %H:%M:%S"

# # print(type(datetime.strptime(s, t)))



# # a = [1,2,5,3,6,7,8]
# # print(a)
# # a.sort()
# # print(a)



# # s = '["A","C"]'


# # print(s.replace("[", "").replace("]", "").replace('"', ""))


a = {
    "a": 1,
    "b": 2
}

asdf = a.pop("a")

print(a, asdf)