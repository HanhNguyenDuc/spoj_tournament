from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import View
from .utils import DataProcessor
from .models import User, Relationship, Problem
import functools

# Create your views here.
LOCAL_TEMP_DIR = '/home/hanhnd/workspace/spoj-tour-web/spoj/rank/templates/rank/'



class RankView(View):
    def get(self, request):
        list_user = list(User.objects.all())
        response_data = {}
        list_user.sort(key = DataProcessor.sort_by_solved_num, reverse=True)
        iterator = -1
        for user in list_user:
            iterator += 1
            # problem_list = DataProcessor.str_to_list(user.solved_list)
            problem_list = Relationship.objects.filter(user_key=user)

            user_ = {}
            user_['rank'] = user.lastrank
            user_['user_name'] = user.name
            user_['solved_num'] = len(problem_list)
            user_['progress_percentage'] = int(min(len(problem_list) / user.target, 1) * 100)
            user_['name'] = user.user_name
            # print(user_)

            
            response_data.update({iterator: user_})
        
        template_ = loader.get_template('rank/rank_2.html')
        print(template_)

        context = {
            'list_user' : response_data,
        }
        return HttpResponse(template_.render(context, request))

class UpdateView(View):
    def get(self, request):
        list_user = list(User.objects.all())
        list_user.sort(key = DataProcessor.sort_by_solved_num, reverse=True)
        iterator = -1

        # Last rank update
        for user in list_user:
            iterator += 1
            user.lastrank = iterator 
            
        be_sorted_list = []
        # Relationship.objects.all().delete()
        for user in list_user:
            problem_list = DataProcessor.get_solved_problems(user.user_url)

            for problem in problem_list:
                query_res = Problem.objects.filter(name=problem)
                # print(len(query_res))
                if len(query_res) == 0:
                    new_problem = Problem(name=problem, score=1)
                    new_problem.save()
                    print("new problem {} has been saved".format(problem))

                prob = Problem.objects.filter(name=problem)[0]
                query_res = Relationship.objects.filter(user_key=user, problem_key=prob)
                # print(len(query_res))
                if len(query_res) == 0:
                    new_obj = Relationship(user_key=user, problem_key=prob)
                    new_obj.save()
                    print("new relationship {} has been saved".format(problem + "-" + user.name))
                

            solved_num = len(problem_list)
            print("{}: ".format(user.user_url))
            print(problem_list)
            if len(problem_list) != 0:
                solved_str = functools.reduce(lambda a, b: "{} {}".format(a, b), problem_list)
            
            # DML
            user.solved_num = solved_num
            user.solved_list = solved_str
            user.save()
            be_sorted_list.append(user)

        # rank update
        be_sorted_list.sort(key = DataProcessor.sort_by_solved_num, reverse=True)
        # for key, user in enumerate(be_sorted_list):
        #     user.lastrank = key + 1
        #     user.save()
        return HttpResponse(content="OK")


class ProblemListingView(View):

    def sort_by_name(self, a):
        return a['problem']

    def sort_by_solved_num(self, a):
        return a['solved_num']


    def get(self, request):
        # user_name = request.GET['user_name']
        response = []
        sort_method = "name"
        # user = User.objects.filter(user_name=user_name)[0]
        problem_list = list(Problem.objects.all())
        user_list = list(User.objects.all())
        user_list_context = []

        for user in user_list:
            user_list_context.append({'user_name': user.user_name, 'name': user.name})


        # relationship_list = Relationship.objects.filter(user_key=user)
        for problem in problem_list:
            # problem = relationship.problem_key
            # list_url.append(problem.get_url())
            # list_problem.append(problem.name)
        
            content = {}
            content['url'] = problem.get_url
            content['problem'] = problem.name
            content['solved_num'] =  len(Relationship.objects.filter(problem_key = problem))

            response.append(content)

        if (sort_method == "name"):
            response.sort(key=self.sort_by_name)
        elif sort_method == "name-reversed":
            response.sort(key=self.sort_by_name, reverse = True)
        elif sort_method == "solved-num":
            response.sort(key=self.sort_by_solved_num)
        elif sort_method == "solved-num-reversed":
            response.sort(key=self.sort_by_solved_num, reverse = True)

        context = {
            'user_list_context': user_list_context,
            'problem_list': response
        }


        template_ = loader.get_template('rank/list.html')

        return HttpResponse(template_.render(context, request))

    def post(self, request):
        # user_name = request.GET['user_name']
        response = []
        sort_method = request.POST['sort-method']
        user_text = request.POST['user']

        # user = User.objects.filter(user_name=user_name)[0]
        problem_list = list(Problem.objects.all())
        user_list = list(User.objects.all())
        user_list_context = []

        for user in user_list:
            user_list_context.append({'user_name': user.user_name, 'name': user.name})
        
        if user_text != "all":

            user = User.objects.filter(user_name=user_text)[0]
            private_list = set(map(lambda a: a.problem_key, Relationship.objects.filter(user_key=user)))
            problem_list = set(problem_list)
            problem_list = list(problem_list.difference(private_list))


        # relationship_list = Relationship.objects.filter(user_key=user)
        for problem in problem_list:
            # problem = relationship.problem_key
            # list_url.append(problem.get_url())
            # list_problem.append(problem.name)
        
            content = {}
            content['url'] = problem.get_url
            content['problem'] = problem.name
            content['solved_num'] =  len(Relationship.objects.filter(problem_key = problem))



            response.append(content)

        if (sort_method == "name"):
            response.sort(key=self.sort_by_name)
        elif sort_method == "name-reversed":
            response.sort(key=self.sort_by_name, reverse = True)
        elif sort_method == "solved-num":
            response.sort(key=self.sort_by_solved_num)
        elif sort_method == "solved-num-reversed":
            response.sort(key=self.sort_by_solved_num, reverse = True)

        context = {
            'user_list_context': user_list_context,
            'problem_list': response
        }


        template_ = loader.get_template('rank/list.html')

        return HttpResponse(template_.render(context, request))

class CompareView(View):
    def get(self, request):

        user_list = User.objects.all()
        user_name_1 = user_list[0].user_name
        user_name_2 = user_list[1].user_name

        context =  self.get_content(user_name_1, user_name_2)

        template_ = loader.get_template('rank/compare_2.html')

        return HttpResponse(template_.render(context, request))
    
    def post(self, request):
        user_name_1 = request.POST['select_1']
        user_name_2 = request.POST['select_2']

        context =  self.get_content(user_name_1, user_name_2)

        template_ = loader.get_template('rank/compare_2.html')

        return HttpResponse(template_.render(context, request))

    def get_pro(self, relationship):
        return relationship.problem_key

    def get_content(self, user_name_1, user_name_2):
        user_list = User.objects.all()

        user_1 = User.objects.filter(user_name=user_name_1)[0]
        user_2 = User.objects.filter(user_name=user_name_2)[0]

        relationship_1 = set(map(self.get_pro, list(Relationship.objects.filter(user_key=User.objects.filter(user_name=user_name_1)[0]))))
        relationship_2 = set(map(self.get_pro, list(Relationship.objects.filter(user_key=User.objects.filter(user_name=user_name_2)[0]))))

        dif_2_1 = relationship_2.difference(relationship_1)
        dif_1_2 = relationship_1.difference(relationship_2)
        
        dif_pro_1_2 = []
        for relationship in dif_1_2:
            pro = relationship
            dif_pro_1_2.append({'problem': pro.name, 'url': pro.get_url()})

        dif_pro_2_1 = []
        for relationship in dif_2_1:
            pro = relationship
            dif_pro_2_1.append({'problem': pro.name, 'url': pro.get_url()})


        user_list_context = []
        for user in user_list:
            user_list_context.append({'name': user.name
                            , 'user_name': user.user_name})

        context = {
            'user_list_context': user_list_context,
            'user_1': {'name': user_1.name, 'user_name': user_1.user_name, 'solved_num': user_1.solved_num},
            'user_2': {'name': user_2.name, 'user_name': user_2.user_name, 'solved_num': user_2.solved_num},
            'dif_pro_1_2_list': dif_pro_1_2,
            'dif_pro_2_1_list': dif_pro_2_1
        }

        return context
        

class CompareResult(View):
    def get(self, request):
        user_name_1 = request.GET['user_1']
        user_name_2 = request.GET['user_2']

        response = []
        relationship_1 = set(Relationship.objects.filter(user_key=User.objects.filter(user_name=user_name_1)[0]))
        relationship_2 = set(Relationship.objects.filter(user_key=User.objects.filter(user_name=user_name_2)[0]))

        dif = relationship_2.difference(relationship_1)
        for relationship in dif:
            response.append({'problem': relationship.problem_key.name,
                            'url': DataProcessor.convert_to_url(relationship.problem_key.name)})

        context = {
            'problem_list': response
        }

        template_ = loader.get_template('rank/compare_result.html')

        return HttpResponse(template_.render(context, request))
        

class ResetRank(View):
    def get(self, request):
        user_list = list(User.objects.all())
        user_list.sort(key=DataProcessor.sort_by_solved_num, reverse=True)
        iterator = -1
        for user in user_list:
            iterator += 1
            user.lastrank = iterator
            user.save()
        
        return HttpResponse(content="OK")

class ResetRelationship(View):
    def get(self, request):
        log = Relationship.objects.all().delete()

        return HttpResponse(content="Deleted all {}".format(log))