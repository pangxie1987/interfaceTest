from locust import TaskSet, HttpLocust, task

xrbiz_url = 'http://172.16.101.224:9200'
Authorization = 'Bearer 99331363-d4bf-47fe-8571-8dba3dd44829'

header_www = {
			'Authorization': Authorization,
			'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
			}
header_json = {
			'Authorization': Authorization,
			'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
			}

class UserBehavior(TaskSet):
	@task(0)
	def project_list(self):
		'项目列表查询'
		payload = {'page':1, 'list':100, }
		r = self.client.post('/api-xrbiz/project/list', data=payload, headers=header_www)
		print(r.text)
		assert r.status_code == 200

	@task(0)
	def getIndustryList(self):
		'行业列表查询'
		payload = {'name':'', 'labelName':''}
		r = self.client.get('/api-xrbiz/industry/getIndustryList', params=payload, headers=header_www)
		print(r.text)
		assert r.status_code == 200

	@task(0)
	def project_update(self):
		'行业列表查询'
		payload = {
			"projectManager": "364",
			"meetingReportFiles": [{"name":"额度信息 (23).xls","createbyDesc":"余湉","createby":364,"createtime":"2020-04-28 14:36:53","code":"5417107895214bc4a35ad29e48854479","type":"application/vnd.ms-excel"}],
			"updateByName": "余湉",
			"projectManagerName": "余湉",
			"projectSource": 3,
			"industry": 24,
			"projectStatusDesc": "正常",
			"scopeDept": 70,
			"orgId": 270,
			"businessPhaseDesc": "尚未展开",
			"createby": 364,
			"labelIds": "",
			"projectSourceUsers": "机构1；机构2；机构三四五",
			"id": "e1447abe989148beb55a4b7bb4594160",
			"projectMember": 364,
			"projectMemberName": "余湉",
			"priorityDesc": "",
			"summary": "000000000000000",
			"createByName": "余湉",
			"interviewSummaryFiles": [{"name":"额度信息 (22) (1).xls","createbyDesc":"余湉","createby":364,"createtime":"2020-04-28 14:36:47","code":"dccf7523b2904edf89f3ffb78454b72f","type":"application/vnd.ms-excel"}],
			"deptId": "kj",
			"updateTime": "2020-04-28 14:41:06",
			"industryDesc": "民航机构",
			"priority": 0,
			"contactIds": "07ac575e267a4a449a9d8eadeaac5c50,cc5163395b13496cbe32305603926fb7",
			"businessPhase": -1,
			"projectStatus": 1,
			"createTime": "2020-04-28 14:35:31",
			"simpleName": "yutian-回归测试4",
			"updateby": 364,
			"name": "yutian-回归测试4",
			"businessId": "e1447abe989148beb55a4b7bb4594160"
		}
		r = self.client.post('/api-xrbiz/project/update', data=payload, headers=header_www)
		print(r.text)
		assert r.status_code == 200

	@task(1)
	def getIndustryList(self):
		'行业列表查询'
		payload = {'bizId':'e1447abe989148beb55a4b7bb4594160', 'bizType':2, 'sysId':1}
		test_url = '/api-commonbiz/document/table'
		r = self.client.post(test_url, data=payload, headers=header_www)
		print(r.text)
		assert r.status_code == 200

class WebsiteUser(HttpLocust):
	task_set=UserBehavior
	min_wait=1
	max_wait=1