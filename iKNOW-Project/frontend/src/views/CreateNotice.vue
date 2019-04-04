<template>
  <div>
    <navigationBar></navigationBar>
    <div class="layout">
      <div class="layout-content">
        <Row>
          <Col span="15">
            <div class="layout-content-main">
              <Form ref="infoForm" :model="infoForm" :rules="ruleinfoForm" :label-width="80">
                <Row>
                  <Col span="5" class="font-style">创建公告</Col>
                </Row>
                <Row style="margin: 0 0 40px 50px">
                  <Col span="22"><hr color="#bbbec4" size="1" /></Col>
                </Row>
                <Row>
                  <Col span="16" offset="4">
                    <FormItem label="标题" prop="title">
                      <Input v-model="infoForm.title" placeholder="请输入公告名称"></Input>
                    </FormItem>
                    <FormItem label="内容" prop="content">
                      <Input v-model="infoForm.content" type="textarea" :autosize="{minRows: 10,maxRows: 20}" placeholder="请输入公告内容"></Input>
                    </FormItem>
                    <FormItem>
                      <Button type="primary" @click="handleSubmit('infoForm')">发布</Button>
                      <Button @click="handleSave('infoForm')" style="margin-left: 8px">暂存</Button>
                      <Button type="ghost" @click="handleCancel('infoForm')" style="float: right">取消</Button>
                    </FormItem>
                  </Col>
                </Row>
              </Form>
            </div>
          </Col>
        </Row>
      </div>
      <div class="layout-copy">
        2011-2017 &copy; iKNOW
      </div>
    </div>
  </div>
</template>
<script>
import navigationBar from '../components/navigationBar'
export default {
  name: 'CreateNotice',
  data () {
    return {
      choosetheme: 'light',
      infoForm: {
        title: '',
        content: ''
      },
      ruleinfoForm: {
        title: [
          { required: true, message: 'The title cannot be empty', trigger: 'blur' }
        ],
        content: [
          { required: true, message: 'The content cannot be empty', trigger: 'blur' }
        ]
      }
    }
  },
  components: {
    navigationBar
  },
  created () {
    if (this.GLOBAL.orgInfoForm.name === '') {
      this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/login')
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.GLOBAL.orgUserId = res.userid
        })
        .catch((response) => {
          this.$Message.error('抱歉,您还未登录')
        })
    }
  },
  methods: {
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.$http.post(this.GLOBAL.baseUrl + 'api/competition/notice', {competition_id: this.$route.params.id, title: this.infoForm.title, content: this.infoForm.content, status: 1})
          .then((response) => {
            this.$Message.success('提交公告信息成功!')
            this.$router.push('/competitionmanage/' + this.$route.params.id)
          })
          .catch((response) => {
            this.$Message.error('提交公告信息失败')
          })
        } else {
          this.$Message.error('您填写的公告信息有误')
        }
      })
    },
    handleSave (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.$http.post(this.GLOBAL.baseUrl + 'api/competition/notice', {competition_id: this.$route.params.id, title: this.infoForm.title, content: this.infoForm.content, status: 0})
          .then((response) => {
            this.$Message.success('保存公告信息成功!')
            this.$router.push('/competitionmanage/' + this.$route.params.id)
          })
          .catch((response) => {
            this.$Message.error('保存公告信息失败')
          })
        } else {
          this.$Message.error('您填写的公告信息有误')
        }
      })
    },
    handleCancel (name) {
      this.$router.push('/competitionmanage/' + this.$route.params.id)
    }
  }
}
</script>

<style scoped>
    .modifyavatar{
      margin: 0 auto;
    }
    .formset{
        margin-left: 210px;
        width: 315px;
    }
    .sidebar{
        background: #f8f8f9;
        z-index: 0;
    }
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        margin-top: 2%;
    }
    .layout-logo{
        width: 100px;
        height: 30px;
        background: #5b6270;
        border-radius: 3px;
        float: left;
        position: relative;
        top: 15px;
        left: 20px;
    }
    .layout-nav{
        width: 420px;
        margin: 0 auto;
    }
    .layout-assistant{
        width: 300px;
        margin: 0 auto;
        height: inherit;
    }
    .layout-breadcrumb{
        padding: 10px 15px 0;
    }
    .layout-content{
        min-height: 100%;
        margin: 15px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
    }
    .layout-content-main{
        padding: 30px 30px 20px 50px;
    }
    .ivu-col-span-15{
        width: 100%;
    }
    .layout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
    .font-style{
        margin-bottom: 10px;
        text-align:center;
        display: inline-block;
        font-size: 25px;
        color: #666;
        font-weight: 600;
        overflow: hidden;
    }
</style>
