import wikipedia
#
ny = wikipedia.page("New York City")

print(ny.title)
print(ny.categories)
print(ny.summary)

# def get_context_list(context, min_len=700):
#     context_list = []
#     assert context
#     p1, p2 = 0, 0
#     while p2 < len(context):
#         p2 += min_len
#         while p2 < len(context) and context[p2] != '.':
#             p2 += 1
#         p2 += 1
#         context_list.append(context[p1:p2])
#         p1 = p2
#     return context_list
#
# print(get_context_list("1234567.ab.c.d.efghij.kl.mnopqr.", min_len=5))