<template>
  <div>
    <navigationBar></navigationBar>
    <div class="layout">
      <div class="layout-content">
        <Row>
          <Col span="15">
            <div class="layout-content-main">
              <Form ref="infoForm" :model="infoForm" :rules="ruleInfoForm" :label-width="80">
                <Row style="margin-left:50px; margin-bottom:20px">
                  <Col span="9"><hr color="#bbbec4" size="1" /></Col>
                  <Col span="5" style="text-align:center; margin-top:-7px;font-size:14px;font-weight:bold">基本信息</Col>
                  <Col span="9"><hr color="#bbbec4" size="1" /></Col>
                </Row>
                <Row>
                  <Col span="5" style="padding:20px 0 0 100px"></Col>
                  <Col span="12" offset="3">
                    <FormItem label="姓名" prop="name">
                      <Input v-model="infoForm.name" placeholder="请输入姓名"></Input>
                    </FormItem>
                    <FormItem label="昵称" prop="nickname">
                      <Input v-model="infoForm.nickname" placeholder="请输入你的昵称"></Input>
                    </FormItem>
                    <FormItem label="性别" prop="gender">
                      <RadioGroup v-model="infoForm.gender">
                        <Radio label=1>男</Radio>
                        <Radio label=2>女</Radio>
                      </RadioGroup>
                    </FormItem>
                    <FormItem label="个人简介" prop="introduction">
                      <Input v-model="infoForm.introduction" type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="请填写你的个人简介"></Input>
                    </FormItem>
                  </Col>
                </Row>
                <Row style="margin:20px 0 20px 50px">
                  <Col span="9"><hr color="#bbbec4" size="1" /></Col>
                  <Col span="5" style="text-align:center;margin-top:-7px;font-size:14px;font-weight:bold">教育信息</Col>
                  <Col span="9"><hr color="#bbbec4" size="1" /></Col>
                </Row>
                <Row>
                  <Col span="5" style="padding:20px 0 0 100px"></Col>
                  <Col span="12" offset="3">
                    <FormItem label="学校" prop="school">
                      <Input v-model="infoForm.school" placeholder="请输入您所在的学校"></Input>
                    </FormItem>
                    <FormItem label="专业" prop="major">
                      <Input v-model="infoForm.major" placeholder="请输入您的专业"></Input>
                    </FormItem>
                    <FormItem label="学号" prop="student_number">
                      <Input v-model="infoForm.student_number" placeholder="请输入您的学号"></Input>
                    </FormItem>
                  </Col>
                </Row>
                <Row style="margin:20px 0 20px 50px">
                  <Col span="9"><hr color="#bbbec4" size="1" /></Col>
                  <Col span="5" style="text-align:center;margin-top:-7px;font-size:14px;font-weight:bold">联系方式</Col>
                  <Col span="9"><hr color="#bbbec4" size="1" /></Col>
                </Row>
                <Row>
                  <Col span="5" style="padding:20px 0 0 100px"></Col>
                  <Col span="12" offset="3">
                    <FormItem label="手机号" prop="phone_number">
                      <Input v-model="infoForm.phone_number" placeholder="请输入手机号"></Input>
                    </FormItem>
                    <FormItem>
                      <Button type="primary" @click="handleSubmit('infoForm')">提交</Button>
                      <Button @click="handleCancel('infoForm')" style="margin-left: 8px">取消</Button>
                      <Button type="ghost" @click="handleReset('infoForm')" style="margin-left: 230px">重置</Button>
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
  name: 'PriPage',
  data () {
    return {
      infoForm: {
        gender: '',
        introduction: this.GLOBAL.priInfoForm.introduction,
        major: this.GLOBAL.priInfoForm.major,
        name: this.GLOBAL.priInfoForm.name,
        nickname: this.GLOBAL.priInfoForm.nickname,
        phone_number: this.GLOBAL.priInfoForm.phone_number,
        school: this.GLOBAL.priInfoForm.school,
        student_number: this.GLOBAL.priInfoForm.student_number
      },
      ruleInfoForm: {
        name: [
          { required: true, message: 'The name cannot be empty', trigger: 'blur' }
        ],
        nickname: [
          { required: true, message: 'The nickname cannot be empty', trigger: 'blur' }
        ],
        introduction: [
          { required: true, message: 'The brief introduction cannot be empty', trigger: 'blur' }
        ],
        major: [
          { required: true, message: 'The major cannot be empty', trigger: 'blur' }
        ],
        student_number: [
          { required: true, message: 'The number cannot be empty', trigger: 'blur' }
        ],
        school: [
          { required: true, message: 'The school cannot be empty', trigger: 'blur' }
        ],
        phone_number: [
          { required: true, message: 'The phone number cannot be empty', trigger: 'blur' }
        ]
      }
    }
  },
  components: {
    navigationBar
  },
  created () {
    if (this.GLOBAL.priInfoForm.name === '') {
      this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/login')
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.GLOBAL.priUserId = res.userid
          this.links()
        })
        .catch((response) => {
          this.$Message.error('抱歉,您还未登录')
        })
    } else {
      this.getGender()
    }
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/modify_pri_info' && from.path === '/pripage') {
        this.infoForm.name = this.GLOBAL.priInfoForm.name
        this.infoForm.nickname = this.GLOBAL.priInfoForm.nickname
        this.infoForm.gender = this.GLOBAL.priInfoForm.gender
        this.infoForm.introduction = this.GLOBAL.priInfoForm.introduction
        this.infoForm.school = this.GLOBAL.priInfoForm.school
        this.infoForm.major = this.GLOBAL.priInfoForm.major
        this.infoForm.student_number = this.GLOBAL.priInfoForm.student_number
        this.infoForm.phone_number = this.GLOBAL.priInfoForm.phone_number
        this.getGender()
      }
    }
  },
  methods: {
    links () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/con_detail/' + this.GLOBAL.priUserId)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.infoForm.name = res.name
          this.infoForm.nickname = res.nickname
          this.infoForm.gender = res.gender
          this.infoForm.introduction = res.introduction
          this.infoForm.school = res.school
          this.infoForm.major = res.major
          this.infoForm.student_number = res.student_number
          this.infoForm.phone_number = res.phone_number
          this.GLOBAL.priInfoForm.name = res.name
          this.GLOBAL.priInfoForm.nickname = res.nickname
          this.GLOBAL.priInfoForm.gender = res.gender
          this.GLOBAL.priInfoForm.phone_number = res.phone_number
          this.GLOBAL.priInfoForm.school = res.school
          this.GLOBAL.priInfoForm.major = res.major
          this.GLOBAL.priInfoForm.student_number = res.student_number
          this.GLOBAL.priInfoForm.introduction = res.introduction
        })
        .catch((response) => {
          this.$Message.error('获取个人信息失败,请重新填写')
        })
    },
    getGender () {
      if (this.GLOBAL.priInfoForm.gender === 'male') {
        this.infoForm.gender = 1
      } else if (this.GLOBAL.priInfoForm.gender === 'female') {
        this.infoForm.gender = 2
      }
    },
    handleSubmit (name) {
      this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/con_detail/' + this.GLOBAL.priUserId, this.infoForm)
      .then((response) => {
        this.GLOBAL.priInfoForm.name = this.infoForm.name
        this.GLOBAL.priInfoForm.nickname = this.infoForm.nickname
        this.GLOBAL.priInfoForm.major = this.infoForm.major
        if (this.infoForm.gender === 1) {
          this.GLOBAL.priInfoForm.gender = 'male'
        } else if (this.infoForm.gender === 2) {
          this.GLOBAL.priInfoForm.gender = 'female'
        }
        this.GLOBAL.priInfoForm.introduction = this.infoForm.introduction
        this.GLOBAL.priInfoForm.phone_number = this.infoForm.phone_number
        this.GLOBAL.priInfoForm.school = this.infoForm.school
        this.GLOBAL.priInfoForm.student_number = this.infoForm.student_number
        this.$Message.success('提交个人信息成功!')
        this.$router.push('/pripage')
      })
      .catch((response) => {
        this.$Message.error('提交个人信息失败')
      })
    },
    handleCancel (name) {
      this.$router.push('/pripage')
    },
    handleReset (name) {
      this.$refs[name].resetFields()
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
        padding: 50px 30px 20px 50px;
    }
    .ivu-col-span-15{
      width: 100%;
    }
    .layout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
</style>
