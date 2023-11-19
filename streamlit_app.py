from openai import OpenAI
import streamlit as st
import time

#asst_VAbeueJgrQ4nCBXsAXblrPix精神康复医院id
jingshenkangfu_id='asst_VAbeueJgrQ4nCBXsAXblrPix'
title_text='😬口袋心理专家😬'
welcome_text='欢迎来到口袋心理专家,你可以问我关于心理健康的问题，例如：有几个月不想说话，我是不是抑郁了？'
wait_prompt='等待投喂问题哦'

print('start--------------------------------------------------')
if 'threadid' not in st.session_state:
	st.session_state['threadid'] = ''
	print('set st.session_state["threadid"] = “”')

threadid=''
print('0')
print(threadid)
client = OpenAI(
	api_key="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"    #赖总
	#api_key="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"  #我的
)

assistant = client.beta.assistants.retrieve(jingshenkangfu_id)#赖总
#assistant = client.beta.assistants.retrieve("asst_0Mhoh0sJHpRIIrx6bHQZPHWh")    #我的
print(assistant)

st.title(title_text)
st.text(welcome_text)
my_bar = st.progress(0, text=wait_prompt)
query = st.chat_input("等待你在这提问哦")

print('session_state threadid : ' + st.session_state['threadid'])

#2.
#create thread or retrieve
#POST v1/threads
if(st.session_state['threadid'] == ''):
	print('thread create')
	thread = client.beta.threads.create()
else:
	print('thread retrieve')
	thread = client.beta.threads.retrieve(st.session_state['threadid'])
st.session_state['threadid'] = thread.id
threadid=thread.id
print('session_state threadid2 : ' + st.session_state['threadid'])
print('threadid: ' + threadid)

print('1')
if query:
	print('2')
	my_bar.progress(10, text='正在查询新华字典')
	#3.create message
	#POST v1/threads/thread_1XaHVN7dWnKxVZASu6sQaD7F/messages
	thread_message = client.beta.threads.messages.create(
		threadid,
		role="user",
		content= query
	)
	print('go：')
	print(thread_message)
	user_message_id = thread_message.id


	#4.
	run = client.beta.threads.runs.create(
               thread_id=threadid,
               assistant_id=assistant.id
	)


	runs = client.beta.threads.runs.list(
		threadid
	)

	
	##################### step
	run_steps = client.beta.threads.runs.steps.list(
    		thread_id=threadid,
    		run_id=run.id
	)
	##################### step
	
	#5.Check the Run status
	while run.status == "queued" or run.status == "in_progress":
		run = client.beta.threads.runs.retrieve(
			thread_id=threadid,
			run_id=run.id,
		)
		time.sleep(0.5)

	my_bar.progress(60, text='找到点头绪了')
	#6.Display the Assistant's Response
	messages = client.beta.threads.messages.list(
  		threadid,
		order='asc'
	)
	

	my_bar.progress(90, text='可以开始生成答案了，脑细胞在燃烧')
	chats = ''
	it = iter(messages)
	for x in it:
		print(x)
		if(x.role=='user'):
			with st.chat_message("human", avatar=None):
				st.write('\n阁下：' + x.content[0].text.value)
		else:
			with st.chat_message("assistant", avatar=None):
				st.write('\n客服：' + x.content[0].text.value)
			
	my_bar.progress(90, text=wait_prompt)
print('end--------------------------------------------------')
