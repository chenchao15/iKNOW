<template>
<div class="orgMsg">
  <h1>组织信息设置</h1><br>
    <Form class="fontsize" style="font-weight:bold" ref="infoForm" :model="infoForm" :rules="ruleValidate" :label-width="110">
    <Row>
      <Col span="9"><hr color="#bbbec4" size="1" /></Col>
      <Col span="4" style="text-align:center;margin-top:-7px;font-size:14px;font-weight:bold">基本信息</Col>
      <Col span="9"><hr color="#bbbec4" size="1" /></Col><br>
    </Row>
    <Row>
      <Col span="15">
        <FormItem label="名称" prop="name">
          <Input style="width:200px" v-model="infoForm.name" placeholder="" disabled></Input>
        </FormItem>
        <FormItem label="简称" prop="abbreviation">
          <Input style="width:200px" v-model="infoForm.abbreviation" placeholder="" disabled></Input>
        </FormItem>
        <FormItem label="简介" prop="briefintro">
          <Input v-model="infoForm.briefintro" type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="" disabled></Input>
        </FormItem>
        <FormItem label="地址" prop="address">
          <Input v-model="infoForm.address" placeholder="" disabled></Input>
        </FormItem>
        <FormItem label="领域" prop="field">
          <Input v-model="infoForm.field" placeholder="" disabled></Input>
        </FormItem>
      </Col>
      <Col span="8">
        <div class="avatar">
          <Row>
            <img style="width:100px;height:100px;border-radius: 100px;" :src="infoForm.avatar_url"/>
            <div class="avatar-cover">
              <Row>
                <Col span='12'><Icon class="iconava-eye" type="ios-eye-outline" @click.native="handleView()"></Icon></Col>
                <Col span='12'>
                  <Upload
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
            <img :src="infoForm.avatar_url" v-if="visible" style="width: 100%">
          </Modal>
        </div>
      </Col>
    </Row>
    <Row>
      <Col span="9"><hr color="#bbbec4" size="1" /></Col>
      <Col span="4" style="text-align:center;margin-top:-7px;font-size:14px;font-weight:bold">联系方式</Col>
      <Col span="9"><hr color="#bbbec4" size="1" /></Col><br>
    </Row>
    <Row>
      <Col span="15">
        <FormItem label="联系人" prop="linkman">
          <Input disabled v-model="infoForm.linkman" placeholder=""></Input>
        </FormItem>
        <FormItem label="手机号" prop="phonenumber">
          <Input disabled v-model="infoForm.phonenumber" placeholder=""></Input>
        </FormItem>
        <FormItem label="邮箱" prop="contact_email">
          <Input disabled v-model="infoForm.contact_email" placeholder=""></Input>
        </FormItem>
      </Col>
    </Row>
    <FormItem>
      <Button type="primary" @click="modifyOrgInfo">编辑</Button>
    </FormItem>
  </Form>
</div>
</template>

<script>
export default {
  name: 'orgMsg',
  data () {
    return {
      visible: false,
      cookie: this.getCookie('csrftoken'),
      infoForm: {
        name: this.GLOBAL.orgInfoForm.name,
        abbreviation: this.GLOBAL.orgInfoForm.abbreviation,
        briefintro: this.GLOBAL.orgInfoForm.briefintro,
        address: this.GLOBAL.orgInfoForm.address,
        field: this.GLOBAL.orgInfoForm.field,
        linkman: this.GLOBAL.orgInfoForm.linkman,
        phonenumber: this.GLOBAL.orgInfoForm.phonenumber,
        contact_email: this.GLOBAL.orgInfoForm.contact_email,
        file_name: this.GLOBAL.orgInfoForm.file_name,
        avatar_url: this.GLOBAL.avatar_url
      }
    }
  },
  created () {
    this.reLinks()
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/orgpage' && from.path === '/modify_org_info') {
        this.links()
      } else if (to.path === '/orgpage') {
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
      this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/org_detail/' + this.GLOBAL.orgUserId)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.infoForm.name = res.name
          this.infoForm.abbreviation = res.shortname
          this.infoForm.briefintro = res.introduction
          this.infoForm.address = res.address
          this.infoForm.field = res.field
          this.infoForm.linkman = res.contact
          this.infoForm.phonenumber = res.contact_number
          this.infoForm.contact_email = res.contact_email
          this.infoForm.file_name = res.file_name
          this.infoForm.avatar_url = res.avatar_url
          this.GLOBAL.orgInfoForm.name = res.name
          this.GLOBAL.orgInfoForm.abbreviation = res.shortname
          this.GLOBAL.orgInfoForm.briefintro = res.introduction
          this.GLOBAL.orgInfoForm.address = res.address
          this.GLOBAL.orgInfoForm.field = res.field
          this.GLOBAL.orgInfoForm.linkman = res.contact
          this.GLOBAL.orgInfoForm.phonenumber = res.contact_number
          this.GLOBAL.orgInfoForm.contact_email = res.contact_email
          this.GLOBAL.avatarUrl = res.avatar_url
          this.GLOBAL.file_name = res.file_name
        })
        .catch((response) => {
          this.$Message.error('获取组织信息失败')
        })
    },
    reLinks () {
      if (this.GLOBAL.orgUserId === -1) {
        this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/login')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.GLOBAL.orgUserId = res.userid
            this.links()
          })
          .catch((response) => {
          })
      } else if (this.GLOBAL.orgUserId !== -1) {
        if (this.GLOBAL.orgInfoForm.name === '') {
          this.links()
        } else {
          this.updateInfo()
        }
      }
    },
    modifyOrgInfo () {
      this.$router.push('/modify_org_info')
    },
    updateInfo () {
      this.infoForm.name = this.GLOBAL.orgInfoForm.name
      this.infoForm.abbreviation = this.GLOBAL.orgInfoForm.abbreviation
      this.infoForm.briefintro = this.GLOBAL.orgInfoForm.briefintro
      this.infoForm.address = this.GLOBAL.orgInfoForm.address
      this.infoForm.field = this.GLOBAL.orgInfoForm.field
      this.infoForm.linkman = this.GLOBAL.orgInfoForm.linkman
      this.infoForm.phonenumber = this.GLOBAL.orgInfoForm.phonenumber
      this.infoForm.contact_email = this.GLOBAL.orgInfoForm.contact_email
      this.infoForm.avatar_url = this.GLOBAL.avatarUrl
      this.infoForm.file_name = this.GLOBAL.orgInfoForm.file_name
    },
    handleSuccess (res, file) {
      this.infoForm.avatar_url = res.avatar_url
      var exdate = new Date() // 获取时间ss
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
