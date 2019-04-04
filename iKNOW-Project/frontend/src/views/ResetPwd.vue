<template>
<div class="main-body">
  <p class="setpwd-font">请重设您的密码</p>
  <Form ref="setpwdForm" :model="setpwdForm" :rules="ruleSetpwdForm">
        <FormItem label="Password" prop="password">
            <Input type="password" v-model="setpwdForm.password" placeholder="重设密码">
            </Input>
        </FormItem>
        <FormItem label="Confirm Password" prop="passwdCheck" style="text-align:left">
            <Input type="password" v-model="setpwdForm.passwdCheck" placeholder="确认密码">
            </Input>
        </FormItem>
        <FormItem>
            <Button type="primary" @click="handleSubmit('setpwdForm')">确定</Button>
        </FormItem>
  </Form>
</div>
</template>

<script>
export default {
  name: 'ResetPwd',
  data () {
    const validatePassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please enter your password'))
      } else {
        if (this.organizationForm.passwdCheck !== '') {
          // 对第二个密码框单独验证
          this.$refs.organizationForm.validateField('passwdCheck')
        }
        callback()
      }
    }
    const validatePassCheck = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please enter your password again'))
      } else if (value !== this.organizationForm.password) {
        callback(new Error('The two input passwords do not match!'))
      } else {
        callback()
      }
    }
    return {
      setpwdForm: {
        password: '',
        passwdCheck: ''
      },
      ruleSetpwdForm: {
        password: [
          { validator: validatePassword, trigger: 'blur' },
          { type: 'string', min: 6, message: 'The password length cannot be less than 6 bits', trigger: 'blur' }
        ],
        passwdCheck: [
          { validator: validatePassCheck, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleSubmit (name) {
      this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/change_password', {password: this.setpwdForm.password, encode_id: this.$route.params.encode_id})
      .then((response) => {
        this.$Message.success('密码重设成功')
        this.$router.push('/login')
      }).catch((response) => {
        this.$message.error('密码重设失败')
      })
    }
  }
}
</script>

<style scoped>
    .main-body{
      width: 300px;
      height: 300px;
    }
    .setpwd-font{
      margin-bottom: 20px;
      color: #495060;
      font-size: 15px;
      font-family: Helvetica;
    }
</style>
