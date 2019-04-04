<template>
<div>
  <navigationBar></navigationBar>
  <Row class="main-body">
    <Col span="6" offset="1">
      <Row><img class="logo-img" src="../assets/logo3.png"/></Row>
      <Row><a class="logo-font">iKNOW</a></Row>
      <Row><a class="logo-font">大数据竞赛平台</a></Row>
    </Col>
    <Col span="10" offset="5">
      <div class="signup-border">
        <Tabs v-model="userType">
          <TabPane label="注册学生账号" name="signupStudent" value="signupStudent">
            <Form class="formset" ref="studentForm" :model="studentForm" :rules="ruleStudentForm" >
              <FormItem label="用户名" prop="username">
                <Input type="text" v-model="studentForm.username" placeholder="Username">
                  <Icon type="ios-person-outline" slot="prepend"></Icon>
                </Input>
              </FormItem>
              <FormItem label="邮箱" prop="email">
                <Input type="email" v-model="studentForm.email" placeholder="Email">
                  <Icon type="ios-email-outline" slot="prepend"></Icon>
                </Input>
              </FormItem>
              <FormItem label="密码" prop="password">
                <Input type="password" v-model="studentForm.password" placeholder="Password">
                  <Icon type="ios-locked-outline" slot="prepend"></Icon>
                </Input>
              </FormItem>
              <FormItem label="再次输入密码" prop="passwdCheck" style="text-align:left">
                <Input type="password" v-model="studentForm.passwdCheck" placeholder="Password again">
                  <Icon type="ios-locked-outline" slot="prepend"></Icon>
                </Input>
              </FormItem>
              <FormItem style="text-align:left">
                <Checkbox class="agreement" v-model="checked" :disabled="disabled" size="small">
                  我已阅读并同意<a href="#/agreement">《iKNOW服务协议》</a>
                </Checkbox>
              </FormItem>
              <FormItem style="margin-top:-4%; text-align:right">
                <span v-if="checked">
                  <Button long="true" size="large" type="primary" @click="handleSubmit('studentForm')">注册</Button>
                </span>
                <span v-else>
                  <Button disabled long="true" size="large" type="primary" @click="handleSubmit('studentForm')">注册</Button>
                </span>
                <span class="directLogin">已有iKNOW账号，<a href="#/login">直接登录 <Icon type="arrow-right-a"></Icon></a></span>
              </FormItem>
            </Form>
          </TabPane>
          <TabPane label="注册组织账号" name="signupOrganization" value="signupOrganization">
            <Form class="formset" ref="organizationForm" :model="organizationForm" :rules="ruleOrganizationForm" >
              <FormItem label="用户名" prop="username">
                <Input type="text" v-model="organizationForm.username" placeholder="Username">
                  <Icon type="ios-person-outline" slot="prepend"></Icon>
                </Input>
              </FormItem>
              <FormItem label="邮箱" prop="email">
                <Input type="email" v-model="organizationForm.email" placeholder="Email">
                  <Icon type="ios-email-outline" slot="prepend"></Icon>
                </Input>
              </FormItem>
              <FormItem label="密码" prop="password">
                <Input type="password" v-model="organizationForm.password" placeholder="Password">
                  <Icon type="ios-locked-outline" slot="prepend"></Icon>
                </Input>
              </FormItem>
              <FormItem label="再次输入密码" prop="passwdCheck" style="text-align:left">
                <Input type="password" v-model="organizationForm.passwdCheck" placeholder="Password again">
                  <Icon type="ios-locked-outline" slot="prepend"></Icon>
                </Input>
              </FormItem>
              <FormItem style="text-align:left">
                <Checkbox class="agreement" v-model="checked" :disabled="disabled" size="small">
                  我已阅读并同意<a href="#/agreement">《iKNOW服务协议》</a>
                </Checkbox>
              </FormItem>
              <FormItem style="margin-top:-4%; text-align:right">
                <span v-if="checked">
                  <Button long="true" size="large" type="primary" @click="handleSubmit('organizationForm')">注册</Button>
                </span>
                <span v-else>
                  <Button disabled long="true" size="large" type="primary" @click="handleSubmit('organizationForm')">注册</Button>
                </span>
                <span class="directLogin">已有iKNOW账号，<a href="#/login">直接登录 <Icon type="arrow-right-a"></Icon></a></span>
              </FormItem>
            </Form>
          </TabPane>
        </Tabs>
      </div>
    </Col>
  </Row>
</div>
</template>

<script>
import navigationBar from '../components/navigationBar'
export default {
  name: 'Signup',
  data () {
    const validateUsername = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入您的用户名'))
      } else {
        this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/username', {params: { username: value }})
        .then((response) => {
          callback()
        })
        .catch((response) => {
          callback(new Error('用户名已注册'))
        })
      }
    }
    const validateEmail = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入您的邮箱'))
      } else {
        this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/email', {params: { email: value }})
        .then((response) => {
          callback()
        })
        .catch((response) => {
          callback(new Error('邮箱已注册'))
        })
      }
    }
    const validateStuPassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入您的密码'))
      } else {
        if (this.studentForm.passwdCheck !== '') {
          // 对第二个密码框单独验证
          this.$refs.studentForm.validateField('passwdCheck')
        }
        callback()
      }
    }
    const validateStuPassCheck = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入您的密码'))
      } else if (value !== this.studentForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    const validateOrgPassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入您的密码'))
      } else {
        if (this.organizationForm.passwdCheck !== '') {
          // 对第二个密码框单独验证
          this.$refs.organizationForm.validateField('passwdCheck')
        }
        callback()
      }
    }
    const validateOrgPassCheck = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入您的密码'))
      } else if (value !== this.organizationForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    return {
      checked: false,
      userType: '',
      studentForm: {
        username: '',
        email: '',
        password: '',
        passwdCheck: ''
      },
      ruleStudentForm: {
        username: [
          { validator: validateUsername, trigger: 'blur' }
        ],
        email: [
          { type: 'email', message: '邮箱格式错误', trigger: 'blur' },
          { validator: validateEmail, trigger: 'blur' }
        ],
        password: [
          { validator: validateStuPassword, trigger: 'blur' },
          { type: 'string', min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
        ],
        passwdCheck: [
          { validator: validateStuPassCheck, trigger: 'blur' }
        ]
      },
      organizationForm: {
        username: '',
        email: '',
        password: '',
        passwdCheck: ''
      },
      ruleOrganizationForm: {
        username: [
          { validator: validateUsername, trigger: 'blur' }
        ],
        email: [
          { type: 'email', message: '邮箱格式错误', trigger: 'blur' },
          { validator: validateEmail, trigger: 'blur' }
        ],
        password: [
          { type: 'string', min: 6, message: '密码长度不能小于6位', trigger: 'blur' },
          { validator: validateOrgPassword, trigger: 'blur' }
        ],
        passwdCheck: [
          { validator: validateOrgPassCheck, trigger: 'blur' }
        ]
      }
    }
  },
  components: {
    navigationBar
  },
  watch: {
    userType: function (value) {
      if (value === 'signupStudent') {
        this.$refs['organizationForm'].resetFields()
      } else {
        this.$refs['studentForm'].resetFields()
      }
    }
  },
  methods: {
    handleSubmit (name) {
      var data = {}
      if (name === 'studentForm') {
        data = {usertype: 0, username: this.studentForm.username, password: this.studentForm.password, email: this.studentForm.email}
      } else {
        data = {usertype: 1, username: this.organizationForm.username, password: this.organizationForm.password, email: this.organizationForm.email}
      }
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/signup', data)
          .then((response) => {
            this.$Message.success('我们给您发送了一份邮件，请查看邮件进行验证')
            this.$router.push('/login')
          }).catch((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.signup === 2) {
              this.$Message.error('无法向您的邮箱发送邮件，请更换正确的邮箱')
            } else if (res.signup === 1) {
              this.$Message.error('注册失败')
            }
          })
        } else {
          this.$Message.error('您填写的信息有误')
        }
      })
    }
  }
}
</script>

<style scoped>
    .main-body{
        margin-top: 100px;
        text-align: center;
    }
    .logo-img{
        padding-top: 100px;
    }
    .logo-font{
        top:0px;
        left:75px;
        color: #495060;
        font-size: 40px;
        font-weight: bold;
        font-style:italic;
        font-family: Helvetica Neue;
    }
    .agreement{
        text-align: left;
        font-weight: normal;
    }
    .directLogin{
        text-align: right;
        font-weight: normal;
    } 
    .signup-border{
        width: 500px;
        height: 525px;
        border: 2px solid #dddee1;
        border-radius: 3px;
        padding: 10px 30px;
        background: #f8f8f9;
    }
    .formset{
        font-weight: bold;
    }
</style>
