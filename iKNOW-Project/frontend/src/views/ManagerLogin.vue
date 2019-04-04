<template>
<div>
  <managerBar></managerBar>
  <Row class="mainBody">
    <Col span="6" offset="1">
      <Row><img class="logo-img" src="../assets/logo3.png"/></Row>
      <Row><a class="logo-font">iKNOW</a></Row>
      <Row><a class="logo-font">大数据竞赛平台</a></Row>
    </Col>
    <Col span="10" offset="5">
      <div class="loginBorder">
        <Tabs>
          <TabPane label="iKNOW管理员登录" name="welcome">
            <Form class="formset" ref="formCustom" :model="formCustom" >
              <FormItem label="管理员账号" prop="username">
                  <Input type="text" v-model="formCustom.username" placeholder="Username">
                      <Icon type="ios-person-outline" slot="prepend"></Icon>
                  </Input>
              </FormItem>
              <FormItem label="管理员密码" prop="password" >
                  <Input type="password" v-model="formCustom.password" placeholder="Password">
                      <Icon type="ios-locked-outline" slot="prepend"></Icon>
                  </Input>
              </FormItem>
              <FormItem style="margin-top:4%; text-align:right">
                  <Button long="true" size="large" type="primary" @click="handleSubmit()">登录</Button>
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
import managerBar from '../components/managerBar'
export default {
  name: 'Login',
  data () {
    return {
      checked: false,
      formCustom: {
        username: '',
        password: ''
      }
    }
  },
  components: {
    managerBar
  },
  methods: {
    handleSubmit () {
      this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/manager_login', {username: this.formCustom.username, password: this.formCustom.password})
      .then((response) => {
        this.$router.push('/admin')
      }).catch((response) => {
        this.$Notice.error({
          title: '登录失败',
          desc: '管理员账号密码错误'
        })
      })
    }
  }
}
</script>

<style scoped>
    .mainBody{
      margin-top: 100px;
      text-align: center;
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
