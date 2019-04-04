<template>
  <div>
    <Row class="title">
      <h1>通知管理</h1>
      <Button class="button_create" @click="createGroupMessage">创建新通知</Button>
    </Row>
    <Row class="content">
      <Collapse v-model="list_value">
        <Panel name="published">
            已发布通知
            <div v-for="(published_group_message, index) in published_group_messages" slot="content" class="font-style">
              <div v-model="published_group_messages[index]" class="content-div">
                <a @click="groupMessageDetails(published_group_message.id)">{{published_group_message.title}}</a>
                <span class="time_style">{{published_group_message.create_time}}</span>
                <hr color="#bbbec4" size="1" style="margin: 4px 0"/>
              </div>
            </div>
        </Panel>
        <Panel name="saving">
            待发布通知
            <Button class="button_delteteall"  @click="deleteAll(saving_group_messages)">清空通知</Button>
            <div v-for="(saving_group_message, index) in saving_group_messages" slot="content" class="font-style">
              <div v-model="saving_group_messages[index]" class="content-div">
                <a @click="groupMessageDetails(saving_group_message.id)">{{saving_group_message.title}}</a>
                <span class="time_style">{{saving_group_message.save_time}}
                <Button class="button_delete" @click="publishGroupMessage(index)">发布通知</Button>
                <Button class="button_delete" @click="editGroupMessage(saving_group_message.id)">修改通知</Button>
                <Button class="button_delete" @click="deleteGroupMessage(saving_group_messages, index)">删除通知</Button></span>
                <hr color="#bbbec4" size="1" style="margin: 4px 0"/>
              </div>
            </div>
        </Panel>
      </Collapse>
    </Row>
  </div>
</template>

<script>
export default {
  name: 'groupMessageManage',
  data () {
    return {
      list_value: 'published',
      published_group_messages: [],
      saving_group_messages: []
    }
  },
  mounted () {
    this.$http.get(this.GLOBAL.baseUrl + 'api/competition/group_message', {params: { competition_id: this.$route.params.id }})
    .then((response) => {
      var res = JSON.parse(response.bodyText)
      this.published_group_messages = res.published_group_messages
      this.saving_group_messages = res.saving_group_messages
    })
  },
  methods: {
    deleteAll (informType, deleteFlag) {
      for (var i in informType) {
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/group_message_status', {group_message_id: informType[i].id, new_status: 2})
        .then((response) => {
          console.log('删除通知成功!')
        })
        .catch((response) => {
          console.log('删除通知失败')
        })
      }
    },
    deleteGroupMessage (informType, index, deleteFlag) {
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/group_message_status', {group_message_id: informType[index].id, new_status: 2})
      .then((response) => {
        this.$Message.success('删除通知成功!')
      })
      .catch((response) => {
        this.$Message.error('删除通知失败')
      })
    },
    publishGroupMessage (index) {
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/group_message_status', {group_message_id: this.saving_group_messages[index].id, new_status: 1})
      .then((response) => {
        this.$Message.success('发布通知成功!')
      })
      .catch((response) => {
        this.$Message.error('发布通知失败')
      })
    },
    editGroupMessage (id) {
      this.$router.push('/editGroupMessage/' + this.$route.params.id + '/' + id)
    },
    createGroupMessage () {
      this.$router.push('/createGroupMessage/' + this.$route.params.id)
    },
    informSort (informType) {
    },
    groupMessageDetails (id) {
      this.$router.push('/groupMessageDetails/' + id)
    }
  }
}
</script>
<style>
  .title{
    margin-bottom: 20px;
  }
  .content{
    font-size: 17px;
    font-weight: bold;
  }
  .font-style{
    font-size: 15px;
    font-weight: 300;
  }
  .content-div{
    margin: 5px 4px 10px 4px;
  }
  .button_delete{
    padding: 0px 4px;
    margin-left: 4px;
    margin-bottom: 4px;
    background: white;
  }
  .time_style{
    color: #bbbec4;
    float: right;
  }
  .button_create{
    margin-top: -40px;
    float: right;
    font-size: 16px;
  }
  .button_delteteall{
    padding: 4px 6px;
    margin-right: 6px;
    margin-top: 3px;
    font-size: 14px;
    float: right;
  }
</style>
