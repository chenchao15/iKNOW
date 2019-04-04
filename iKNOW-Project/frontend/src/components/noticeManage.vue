<template>
  <div>
    <Row class="title">
      <h1>公告管理</h1>
      <Button class="button_create" @click="createNotice">创建新公告</Button>
    </Row>
    <Row class="content">
      <Collapse v-model="list_value">
        <Panel name="published">
            已发布公告
            <Button class="button_delteteall"  @click="deleteAll(published_notices)">清空公告</Button>
            <div v-for="(published_notice, index) in published_notices" slot="content" class="font-style">
              <div v-model="published_notices[index]" class="content-div">
                <a @click="noticeDetails(published_notice.id)">{{published_notice.title}}</a>
                <span class="time_style">{{published_notice.create_time}}
                <Button class="button_delete" @click="deleteNotice(published_notices, index)">删除公告</Button></span>
                <hr color="#bbbec4" size="1" style="margin: 4px 0"/>
              </div>
            </div>
        </Panel>
        <Panel name="saving">
            待发布公告
            <Button class="button_delteteall"  @click="deleteAll(saving_notices)">清空公告</Button>
            <div v-for="(saving_notice, index) in saving_notices" slot="content" class="font-style">
              <div v-model="saving_notices[index]" class="content-div">
                <a @click="noticeDetails(saving_notice.id)">{{saving_notice.title}}</a>
                <span class="time_style">{{saving_notice.save_time}}
                <Button class="button_delete" @click="publishNotice(index)">发布公告</Button>
                <Button class="button_delete" @click="editNotice(saving_notice.id)">修改公告</Button>
                <Button class="button_delete" @click="deleteNotice(saving_notices, index)">删除公告</Button></span>
                <hr color="#bbbec4" size="1" style="margin: 4px 0"/>
              </div>
            </div>
        </Panel>
        <Panel name="recyclebin">
            回收站
            <Button class="button_delteteall"  @click="deleteAll(deleted_notices, 'deleted')">彻底清除</Button>
            <div v-for="(deleted_notice, index) in deleted_notices" slot="content" class="font-style">
              <div v-model="deleted_notices[index]" class="content-div">
                <a @click="noticeDetails(deleted_notice.id)">{{deleted_notice.title}}</a>
                <span class="time_style">{{deleted_notice.delete_time}}
                <Button class="button_delete" @click="recoverNotice(index)">恢复公告</Button>
                <Button class="button_delete" @click="deleteNotice(deleted_notices, index, 'deleted')">清除公告</Button></span>
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
  name: 'noticeManage',
  data () {
    return {
      list_value: 'published',
      published_notices: [],
      saving_notices: [],
      deleted_notices: []
    }
  },
  created () {
    this.$http.get(this.GLOBAL.baseUrl + 'api/competition/notice', {params: { competition_id: this.$route.params.id }})
    .then((response) => {
      var res = JSON.parse(response.bodyText)
      this.published_notices = res.published_notices
      this.saving_notices = res.saving_notices
      this.deleted_notices = res.deleted_notices
    })
  },
  watch: {
    '$route' (to, from) {
      if (from.path === '/competitionmanage/' + this.$route.params.id) {
        if (to.path === '/competitionmanage/' + this.$route.params.id) {
          this.links()
        }
      }
    }
  },
  methods: {
    deleteAll (noticeType, deleteFlag) {
      if (deleteFlag === 'deleted') {
        for (var i in noticeType) {
          this.$http.post(this.GLOBAL.baseUrl + 'api/competition/notice_status', {notice_id: noticeType[i].id, new_status: 3})
          .then((response) => {
            console.log('删除公告成功!')
          })
          .catch((response) => {
            console.log('删除公告失败')
          })
        }
      } else {
        for (i in noticeType) {
          this.$http.post(this.GLOBAL.baseUrl + 'api/competition/notice_status', {notice_id: noticeType[i].id, new_status: 2})
          .then((response) => {
            console.log('删除公告成功!')
          })
          .catch((response) => {
            console.log('删除公告失败')
          })
        }
      }
    },
    deleteNotice (noticeType, index, deleteFlag) {
      if (deleteFlag === 'deleted') {
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/notice_status', {notice_id: noticeType[index].id, new_status: 3})
        .then((response) => {
          this.$Message.success('删除公告成功!')
        })
        .catch((response) => {
          this.$Message.error('删除公告失败')
        })
      } else {
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/notice_status', {notice_id: noticeType[index].id, new_status: 2})
        .then((response) => {
          this.$Message.success('删除公告成功!')
        })
        .catch((response) => {
          this.$Message.error('删除公告失败')
        })
      }
    },
    recoverNotice (index) {
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/notice_status', {notice_id: this.deleted_notices[index].id, new_status: 0})
      .then((response) => {
        this.$Message.success('恢复公告成功!')
      })
      .catch((response) => {
        this.$Message.error('恢复公告失败')
      })
    },
    publishNotice (index) {
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/notice_status', {notice_id: this.saving_notices[index].id, new_status: 1})
      .then((response) => {
        this.$Message.success('发布公告成功!')
      })
      .catch((response) => {
        this.$Message.error('发布公告失败')
      })
    },
    editNotice (id) {
      this.$router.push('/editNotice/' + this.$route.params.id + '/' + id)
    },
    createNotice () {
      console.log(this.$route.params.id)
      this.$router.push('/createNotice/' + this.$route.params.id)
    },
    noticeSort (informType) {
    },
    noticeDetails (id) {
      this.$router.push('/noticeDetails/' + id)
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
