<template>
<div>
  <navigationBar></navigationBar>
  <Row class="mainBody">
    <Col span="6" offset="1">
      <Row><img class="logo-img" src="../assets/logo3.png"/></Row>
      <Row><a class="logo-font">iKNOW</a></Row>
      <Row><a class="logo-font">大数据竞赛平台</a></Row>
    </Col>
    <Col span="10" offset="5">
      <div class="loginBorder">
        <Tabs>
          <TabPane label="欢迎来到iKNOW" name="welcome">
            <Form class="formset" ref="formCustom" :model="formCustom" :rules="ruleCustom" >
              <FormItem label="用户名" prop="username">
                  <Input type="text" v-model="formCustom.username" placeholder="Username">
                      <Icon type="ios-person-outline" slot="prepend"></Icon>
                  </Input>
              </FormItem>
              <FormItem label="密码" prop="password" >
                  <Input type="password" v-model="formCustom.password" placeholder="Password">
                      <Icon type="ios-locked-outline" slot="prepend"></Icon>
                  </Input>
              </FormItem>
              <Row>
                <Col span="6">
                  <Checkbox class="rememberPassword" v-model="checked" :disabled="disabled" size="small">
                    一周内记住密码
                  </Checkbox>
                </Col>
                <Col span="4" offset="14">
                  <a class="forgetPassword" href="#/forget_password">忘记密码？</a>
                </Col>
              </Row>
              <FormItem style="margin-top:4%; text-align:right">
                  <Button long="true" size="large" type="primary" @click="handleSubmit('formCustom')">登录</Button>
                  <span class="goSignup">还没有iKNOW账号，<a href="#/signup">立即注册 <Icon type="arrow-right-a"></Icon></a></span>
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
  name: 'Login',
  data () {
    const validateUsername = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入您的用户名'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入您的密码'))
      } else {
        callback()
      }
    }
    return {
      checked: false,
      formCustom: {
        username: '',
        password: ''
      },
      ruleCustom: {
        username: [
          { validator: validateUsername, trigger: 'blur' }
        ],
        password: [
          { type: 'string', min: 6, message: '密码长度不能小于6位', trigger: 'blur' },
          { validator: validatePassword, trigger: 'blur' }
        ]
      }
    }
  },
  components: {
    navigationBar
  },
  // 页面加载调用获取cookie值
  mounted () {
    this.getCookie()
  },
  methods: {
    // 设置 cookie
    setCookie (name, pwd, exdays) {
      var exdate = new Date() // 获取时间
      exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * exdays) // 保存的天数
      // 字符串拼接 cookie
      window.document.cookie = 'username=' + name + ';path=/;expires=' + exdate.toGMTString()
      window.document.cookie = 'password=' + pwd + ';path=/;expires=' + exdate.toGMTString()
    },
    // 读取 cookie
    getCookie () {
      if (document.cookie.length > 0) {
        var arr = document.cookie.split('; ') // 这里显示的格式需要切割一下自己可输出看下
        for (var i = 0; i < arr.length; i++) {
          var arr2 = arr[i].split('=') // 再次切割
          // 判断查找相对应的值
          if (arr2[0] === 'username') {
            this.formCustom.username = arr2[1] // 保存到保存数据的地方
          } else if (arr2[0] === 'password') {
            this.formCustom.password = arr2[1]
          }
        }
      }
    },
    // 清除 cookie
    clearCookie () {
      this.setCookie('', '', -1) // 修改2值都为空，天数为负1天就好了
    },
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          if (this.checked === true) {
            // 传入账号名，密码，和保存天数3个参数
            this.setCookie(this.formCustom.username, this.formCustom.password, 7)
          } else {
            this.clearCookie()
          }
          this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/login', {username: this.formCustom.username, password: this.formCustom.password})
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.$Message.success('登录成功')
            var exdate = new Date() // 获取时间
            exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * 7) // 保存的天数
            this.GLOBAL.islogin = 1
            this.GLOBAL.userType = res.usertype
            if (res.usertype === 0) {
              this.GLOBAL.priUserId = res.userid
            } else if (res.usertype === 1) {
              this.GLOBAL.orgUserId = res.userid
            }
            this.GLOBAL.avatarUrl = res.avatar_url
            window.document.cookie = 'islogin=' + 1 + ';path=/;expires=' + exdate.toGMTString()
            window.document.cookie = 'usertype=' + res.usertype + ';path=/;expires=' + exdate.toGMTString()
            window.document.cookie = 'userid=' + res.userid + ';path=/;expires=' + exdate.toGMTString()
            window.document.cookie = 'avatarurl=' + res.avatar_url + ';path=/;expires=' + exdate.toGMTString()
            this.$router.push('/home')
          }).catch((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.login === 1) {
              this.$Message.error('用户名或密码错误')
            } else if (res.login === 2) {
              this.$Message.error('用户未激活')
            }
          })
        } else {
          this.$Message.error('Incorrect username or password!')
        }
      })
    },
    // 设置登录状态cookie
    setLoginStatusCookie (islogin, usertype, userid, avatarurl, exdays) {
      console.log('后一个' + avatarurl)
      var exdate = new Date() // 获取时间
      exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * exdays) // 保存的天数
      // 字符串拼接 cookie
      this.GLOBAL.islogin = islogin
      window.document.cookie = 'islogin=' + islogin + ';path=/;expires=' + exdate.toGMTString()
      this.GLOBAL.avatarUrl = avatarurl
      window.document.cookie = 'avatarurl=' + avatarurl + ';path=/;expires=' + exdate.toGMTString()
      this.GLOBAL.userType = usertype
      window.document.cookie = 'usertype=' + usertype + ';path=/;expires=' + exdate.toGMTString()
      window.document.cookie = 'userid=' + userid + ';path=/;expires=' + exdate.toGMTString()
    }
  }
}
</script>

<style scoped>
    .mainBody{
        margin-top: 100px;
        text-align: center;
    }
    .logostyle{
        margin-top: 150px;
        margin-left: 200px;
    }
    .logo-img{
        padding-top: 20px;
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
    .operatePwd{
        margin:0 auto;
        text-align:center;
        margin-top:-4%;
    }
    .forgetPassword{
        text-align: right;
        font-weight: normal;
    }
    .rememberPassword{
        text-align: left;
        font-weight: normal;
    }
    .goSignup{
        text-align: right;
        font-weight: normal;
    }
    .loginBorder{
        width: 500px;
        height: 345px;
        border: 2px solid #dddee1;
        border-radius: 3px;
        padding: 10px 30px;
        background: #f8f8f9;
    }
    .formset{
        font-weight: bold;
    }
</style>
