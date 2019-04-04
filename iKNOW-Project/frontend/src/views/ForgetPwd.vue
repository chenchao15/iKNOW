<template>
<div class="main-body">
  <p class="send-font">请输入您的注册邮箱重设密码</p>
  <Form ref="sendForm" :model="sendForm" :rules="ruleSendForm">
        <FormItem prop="email">
            <Input type="email" v-model="sendForm.email" placeholder="请输入您的注册邮箱">
            </Input>
        </FormItem>
        <FormItem>
            <Button type="primary" @click="handleSubmit('sendForm')">发送</Button>
        </FormItem>
  </Form>
</div>
</template>

<script>
export default {
  name: 'ForgetPwd',
  data () {
    return {
      sendForm: {
        email: ''
      },
      ruleSendForm: {
        email: [
          { required: true, message: 'Email cannot be empty', trigger: 'blur' },
          { type: 'email', message: 'Incorrect email format', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/forget_password', {email: this.sendForm.email})
            .then((response) => {
              // var res = JSON.parse(response.bodyText)
              this.$Message.success('发送成功，请注意查收邮件')
              this.$router.push('/home')
            })
            .catch((response) => {
              this.$Message.error('发送失败')
            })
        } else {
          this.$Message.error('发送失败')
        }
      })
    }
  }
}
</script>

<style scoped>
    .main-body{
      width: 300px;
      height: 200px;
    }
    .send-font{
      margin-bottom: 20px;
      color: #495060;
      font-size: 15px;
      font-family: Helvetica;
    }
</style>
