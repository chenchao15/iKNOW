<template>
  <div class="priMsg">
  <h1>个人信息设置</h1><br>
    <Form class="fontsize" style="font-weight:bold" ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="90">
      <Row>
        <Col span="9"><hr color="#bbbec4" size="1" /></Col>
        <Col span="4" style="text-align:center;margin-top:-7px;font-size:14px;font-weight:bold">基本信息</Col>
        <Col span="9"><hr color="#bbbec4" size="1" /></Col><br>
      </Row>
      <Row>
        <Col span="15">
          <FormItem label="姓名" prop="name">
            <Input style="width:200px" v-model="formValidate.name" placeholder="" disabled></Input>
          </FormItem>
          <FormItem label="昵称" prop="nickname">
            <Input style="width:200px" v-model="formValidate.nickname" placeholder="" disabled></Input>
          </FormItem>
          <FormItem label="性别" prop="gender">
            <RadioGroup v-model="formValidate.gender">
              <Radio label="male" disabled>男</Radio>
              <Radio label="female" disabled>女</Radio>
            </RadioGroup>
          </FormItem>
          <FormItem label="介绍" prop="introduction">
            <Input v-model="formValidate.introduction" type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="" disabled></Input>
          </FormItem>
        </Col>
        <Col span="8">
          <div class="avatar">
            <Row>
              <img style="width:100px;height:100px;border-radius: 100px;" :src="formValidate.avatar_url"/>
              <div class="avatar-cover">
                <Row>
                  <Col span='12'><Icon class="iconava-eye" type="ios-eye-outline" @click.native="handleView()"></Icon></Col>
                  <Col span='12'>
                    <Upload
                      :before-upload="handleUpload"
                      :on-success="handleSuccess"
                      :on-error="handleFail"
                      :format="['jpg','jpeg','png','bmp']"
                      :show-upload-list="false"
                      :max-size="2048"
                      :on-format-error="handleFormatError"
                      :on-exceeded-size="handleMaxSize"
                      :action="this.GLOBAL.baseUrl + 'api/userpage/avatar_upload'"
                      :headers="{
                        'X-CSRFToken':cookie
                      }">
                      <Icon class="iconava-upload" type="ios-cloud-upload-outline"></Icon>
                    </Upload>
                  </Col>
                </Row>
              </div>
            </Row>
            <Modal title="View Image" v-model="visible">
              <img :src="formValidate.avatar_url" v-if="visible" style="width: 100%">
            </Modal>
          </div>
        </Col>
      </Row>
      <Row>
        <Col span="9"><hr color="#bbbec4" size="1" /></Col>
        <Col span="4" style="text-align:center;margin-top:-7px;font-size:14px;font-weight:bold">教育信息</Col>
        <Col span="9"><hr color="#bbbec4" size="1" /></Col><br>
      </Row>
      <Row>
        <FormItem label="学校" prop="school">
          <Input style="width:200px" v-model="formValidate.school" placeholder="" disabled></Input>
        </FormItem>
        <FormItem label="专业" prop="major">
          <Input style="width:200px" v-model="formValidate.major" placeholder="" disabled></Input>
        </FormItem>
        <FormItem label="学号" prop="student_number">
          <Input style="width:200px" v-model="formValidate.student_number" placeholder="" disabled></Input>
        </FormItem>
      </Row>
      <Row>
        <Col span="9"><hr color="#bbbec4" size="1" /></Col>
        <Col span="4" style="text-align:center;margin-top:-7px;font-size:14px;font-weight:bold">联系方式</Col>
        <Col span="9"><hr color="#bbbec4" size="1" /></Col><br>
      </Row>
      <Row>
        <Col span="15">
          <FormItem label="手机号" prop="phone_number">
            <Input style="width:200px" v-model="formValidate.phone_number" placeholder="" disabled></Input>
          </FormItem>
        </Col>
      </Row>
      <FormItem>
        <Button type="primary" @click="modifyPriInfo">编辑</Button>
      </FormItem>
    </Form>
  </div>
</template>

<script>
export default {
  name: 'priMsg',
  data () {
    return {
      visible: false,
      cookie: this.getCookie('csrftoken'),
      formValidate: {
        name: this.GLOBAL.priInfoForm.name,
        nickname: this.GLOBAL.priInfoForm.nickname,
        phone_number: this.GLOBAL.priInfoForm.phone_number,
        gender: this.GLOBAL.priInfoForm.gender,
        school: this.GLOBAL.priInfoForm.school,
        major: this.GLOBAL.priInfoForm.major,
        student_number: this.GLOBAL.priInfoForm.student_number,
        introduction: this.GLOBAL.priInfoForm.introduction,
        avatar_url: this.GLOBAL.avatarUrl
      }
    }
  },
  created () {
    this.reLinks()
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/pripage' && from.path === '/modify_pri_info') {
        this.links()
      } else if (to.path === '/pripage') {
        this.cookie = this.getCookie('csrftoken')
        this.reLinks()
      }
    }
  },
  methods: {
    getCookie (name) {
      let reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)')
      let arr
      if ((arr = document.cookie.match(reg))) {
        return decodeURIComponent(arr[2])
      }
    },
    links () {
      this.$http.get('http://127.0.0.1:8000/api/userpage/con_detail/' + this.GLOBAL.priUserId)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.formValidate.name = res.name
          this.formValidate.nickname = res.nickname
          if (res.gender === 1) {
            this.formValidate.gender = 'male'
            this.GLOBAL.priInfoForm.gender = 'male'
          } else if (res.gender === 2) {
            this.formValidate.gender = 'female'
            this.GLOBAL.priInfoForm.gender = 'female'
          }
          this.formValidate.introduction = res.introduction
          this.formValidate.school = res.school
          this.formValidate.major = res.major
          this.formValidate.student_number = res.student_number
          this.formValidate.phone_number = res.phone_number
          if (res.avatar_url === 'static/img/avatar/default_avatar.png') {
            this.formValidate.avatar_url = 'https://i.loli.net/2017/11/30/5a1ee56146906.jpeg'
          } else {
            this.formValidate.avatar_url = res.avatar_url
          }
          this.GLOBAL.priInfoForm.name = res.name
          this.GLOBAL.priInfoForm.nickname = res.nickname
          this.GLOBAL.priInfoForm.phone_number = res.phone_number
          this.GLOBAL.priInfoForm.school = res.school
          this.GLOBAL.priInfoForm.major = res.major
          this.GLOBAL.priInfoForm.student_number = res.student_number
          this.GLOBAL.priInfoForm.introduction = res.introduction
          this.GLOBAL.avatarUrl = res.avatar_url
        })
        .catch((response) => {
          this.$Message.error('获取个人信息失败')
        })
    },
    reLinks () {
      if (this.GLOBAL.priUserId === -1) {
        this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/login')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.GLOBAL.priUserId = res.userid
            this.links()
          })
          .catch((response) => {
          })
      } else if (this.GLOBAL.priUserId !== -1) {
        if (this.GLOBAL.priInfoForm.name === '') {
          this.links()
        } else {
          this.updateInfo()
        }
      }
    },
    modifyPriInfo () {
      this.$router.push('/modify_pri_info')
    },
    updateInfo () {
      this.formValidate.name = this.GLOBAL.priInfoForm.name
      this.formValidate.nickname = this.GLOBAL.priInfoForm.nickname
      this.formValidate.phone_number = this.GLOBAL.priInfoForm.phone_number
      this.formValidate.gender = this.GLOBAL.priInfoForm.gender
      this.formValidate.school = this.GLOBAL.priInfoForm.school
      this.formValidate.major = this.GLOBAL.priInfoForm.major
      this.formValidate.student_number = this.GLOBAL.priInfoForm.student_number
      this.formValidate.introduction = this.GLOBAL.priInfoForm.introduction
      this.formValidate.avatar_url = this.GLOBAL.avatarUrl
    },
    handleSuccess (res, file) {
      this.formValidate.avatar_url = res.avatar_url
      var exdate = new Date() // 获取时间
      exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * 7) // 保存的天数
      window.document.cookie = 'avatarurl=' + res.avatar_url + ';path=/;expires=' + exdate.toGMTString()
      this.$Message.success('上传成功')
    },
    handleFail (file) {
      this.$Message.success('上传失败，请重新上传')
    },
    handleFormatError (file) {
      this.$Notice.warning({
        title: '文件类型错误',
        desc: '文件' + file.name + '的格式或类型不正确, 请上传图片格式文件(jpg,jpeg,png or bmp).'
      })
    },
    handleMaxSize (file) {
      this.$Notice.warning({
        title: '文件大小错误',
        desc: '文件' + file.name + '过大, 请上传不超过２M的文件.'
      })
    },
    handleView () {
      this.visible = true
    },
    handleUpload (file) {
      console.log(file)
    }
  }
}
</script>

<style>
    .avatar{
        position: relative;
        width: 100px;
        padding-top:20px;
    }
    .avatar img{
        width:100px;
        height:100px;
        border-radius: 100px;
        border: 1px solid #dddee1;
    }
    .avatar-cover{
        display: none;
        position: absolute;
        width: 100px;
        height: 100px;
        top: 0px;
        border-radius:100px;
        background: rgba(0,0,0,.6);
    }
    .avatar:hover .avatar-cover{
        display: block;
    }
    .iconava-eye{
        color: #fff;
        font-size: 30px;
        cursor: pointer;
        margin-left: 20px;
        margin-top: 35px;
    }
    .iconava-upload{
        color: #fff;
        font-size: 23px;
        cursor: pointer;
        margin-left: 10px;
        margin-top: 38px;
    }
    .fontsize label{
        font-size: 16px !important;
    }
</style>
