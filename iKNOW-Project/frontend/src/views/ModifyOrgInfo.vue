<template>
  <div>
    <navigationBar></navigationBar>
    <div class="layout">
      <div class="layout-content">
        <div class="layout-content-main">
          <Form ref="infoForm" :model="infoForm" :rules="ruleInfoForm" :label-width="100">
            <Row style="margin-left:50px; margin-bottom:20px">
              <Col span="9"><hr color="#bbbec4" size="1" /></Col>
              <Col span="5" style="text-align:center; margin-top:-7px;font-size:14px;font-weight:bold">基本信息</Col>
              <Col span="9"><hr color="#bbbec4" size="1" /></Col>
            </Row>
            <Row>
              <Col span="5" style="padding:20px 0 0 100px"></Col>
              <Col span="12" offset="3">
                <FormItem label="名称" prop="name">
                  <Input v-model="infoForm.name" placeholder="请输入组织名称"></Input>
                </FormItem>
                <FormItem label="简称" prop="abbreviation">
                  <Input v-model="infoForm.abbreviation" placeholder="请输入组织的简称"></Input>
                </FormItem>
                <FormItem label="简介" prop="briefintro">
                  <Input v-model="infoForm.briefintro" type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="请输入组织的简介"></Input>
                </FormItem>
                <FormItem label="地址" prop="address">
                  <Input v-model="infoForm.address" placeholder="请输入组织所在的地址"></Input>
                </FormItem>
                <FormItem label="领域" prop="field">
                  <Input v-model="infoForm.field" placeholder="请输入组织涉及的领域"></Input>
                </FormItem>
                <!--<FormItem label="组织资料上传">
                  <Upload
                    :before-upload="handleUpload"
                    action="//jsonplaceholder.typicode.com/posts/"
                    :headers="{
                      'X-CSRFToken':cookie
                    }">
                    <Button type="ghost" icon="ios-cloud-upload-outline">选择文件上传（请上传pdf文件）</Button>
                  </Upload>
                  <div v-if="file !== null">文件名: {{ infoForm.file_name }}</div>
                </FormItem>-->
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
                <FormItem label="联系人" prop="linkman">
                  <Input v-model="infoForm.linkman" placeholder="请输入联系人的姓名"></Input>
                </FormItem>
                <FormItem label="手机号码" prop="phonenumber">
                  <Input v-model="infoForm.phonenumber" placeholder="请输入联系人的手机号码"></Input>
                </FormItem>
                <FormItem label="邮箱" prop="contact_email">
                  <Input type="email" v-model="infoForm.contact_email" placeholder="请输入组织的邮箱"></Input>
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
  name: 'OrgPage',
  data () {
    return {
      file: null,
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
        file_name: this.GLOBAL.orgInfoForm.file_name
      },
      ruleInfoForm: {
        name: [
          { required: true, message: '组织名称不能为空', trigger: 'blur' }
        ],
        abbreviation: [
          { required: true, message: '组织简称不能为空', trigger: 'blur' }
        ],
        briefintro: [
          { required: true, message: '组织简介不能为空', trigger: 'blur' }
        ],
        address: [
          { required: true, message: '地址不能为空', trigger: 'blur' }
        ],
        field: [
          { required: true, message: '组织领域不能为空', trigger: 'blur' }
        ],
        linkman: [
          { required: true, message: '组织联系人不能为空', trigger: 'blur' }
        ],
        phonenumber: [
          { required: true, message: '手机号码不能为空', trigger: 'blur' }
        ],
        contact_email: [
          { required: true, message: '组织官方邮箱不能为空', trigger: 'blur' },
          { type: 'email', message: '邮箱格式错误', trigger: 'blur' }
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
          this.links()
        })
        .catch((response) => {
          this.$Message.error('抱歉,您还未登录')
        })
    }
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/modify_org_info' && from.path === '/orgpage') {
        this.infoForm.name = this.GLOBAL.orgInfoForm.name
        this.infoForm.abbreviation = this.GLOBAL.orgInfoForm.abbreviation
        this.infoForm.briefintro = this.GLOBAL.orgInfoForm.briefintro
        this.infoForm.address = this.GLOBAL.orgInfoForm.address
        this.infoForm.field = this.GLOBAL.orgInfoForm.field
        this.infoForm.linkman = this.GLOBAL.orgInfoForm.linkman
        this.infoForm.phonenumber = this.GLOBAL.orgInfoForm.phonenumber
        this.infoForm.contact_email = this.GLOBAL.orgInfoForm.contact_email
        this.infoForm.file_name = this.GLOBAL.orgInfoForm.file_name
      }
    }
  },
  methods: {
    links () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/con_detail/' + this.GLOBAL.orgUserId)
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
          this.infoFor.file_name = res.file_name
          this.GLOBAL.orgInfoForm.name = res.name
          this.GLOBAL.orgInfoForm.abbreviation = res.shortname
          this.GLOBAL.orgInfoForm.briefintro = res.introduction
          this.GLOBAL.orgInfoForm.address = res.address
          this.GLOBAL.orgInfoForm.field = res.field
          this.GLOBAL.orgInfoForm.linkman = res.contact
          this.GLOBAL.orgInfoForm.phonenumber = res.contact_number
          this.GLOBAL.orgInfoForm.contact_email = res.contact_email
          this.GLOBAL.file_name = res.file_name
        })
        .catch((response) => {
          this.$Message.error('获取组织信息失败,请重新填写')
        })
    },
    getCookie (name) {
      let reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)')
      let arr
      if ((arr = document.cookie.match(reg))) {
        return decodeURIComponent(arr[2])
      }
    },
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/org_detail/' + this.GLOBAL.orgUserId, {name: this.infoForm.name, shortname: this.infoForm.abbreviation, introduction: this.infoForm.briefintro, address: this.infoForm.address, field: this.infoForm.field, contact: this.infoForm.linkman, contact_number: this.infoForm.phonenumber, contact_email: this.infoForm.contact_email, file_name: this.infoForm.file_name, file_url: ''})
          .then((response) => {
            this.GLOBAL.orgInfoForm.name = this.infoForm.name
            this.GLOBAL.orgInfoForm.abbreviation = this.infoForm.abbreviation
            this.GLOBAL.orgInfoForm.briefintro = this.infoForm.briefintro
            this.GLOBAL.orgInfoForm.address = this.infoForm.address
            this.GLOBAL.orgInfoForm.field = this.infoForm.field
            this.GLOBAL.orgInfoForm.linkman = this.infoForm.linkman
            this.GLOBAL.orgInfoForm.phonenumber = this.infoForm.phonenumber
            this.GLOBAL.orgInfoForm.contact_email = this.infoForm.contact_email
            this.GLOBAL.orgInfoForm.avatar_url = this.infoForm.avatar_url
            this.GLOBAL.orgInfoForm.file_name = this.infoForm.file_name
            console.log(this.file) // 将this.file传回后端，后端只需要做出其file_url并加到组织者信息里即可
            this.$Message.success('提交组织信息成功!')
            this.$router.push('/orgpage')
          })
          .catch((response) => {
            this.$Message.error('提交组织信息失败')
          })
        } else {
          this.$Message.error('您填写的信息有误')
        }
      })
    },
    handleUpload (file) {
      var name = file.name
      var len = name.length
      if (name[len - 1] === 'f' && name[len - 2] === 'd' && name[len - 3] === 'p') {
        this.file = file
        this.infoForm.file_name = file.name
      } else {
        this.handleFormatError(file)
      }
      return false
    },
    handleFormatError (file) {
      this.$Notice.warning({
        title: '文件类型错误',
        desc: '文件' + file.name + '的格式或类型不正确, 请上传pdf格式文件，或注意文件是否有后缀名.'
      })
    },
    handleCancel (name) {
      this.$router.push('/orgpage')
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
