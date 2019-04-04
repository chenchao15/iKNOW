<template>
<div>
  <div v-if="isvalidate == 1">
    <p class="validate-font">验证成功！</p>
    <a href="#/home">点击前往 iKNOW 主页</a>
  </div>
  <div v-if="isvalidate == 2">
    <p class="validate-font">您已成功验证！</p>
    <a href="#/home">点击前往 iKNOW 主页</a>
  </div>
</div>
</template>

<script>
export default {
  name: 'ValidateEmail',
  data () {
    return {
      isvalidate: 0
    }
  },
  created () {
    this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/validate_email', {encode_id: this.$route.params.encode_id})
    .then((response) => {
      var res = JSON.parse(response.bodyText)
      this.isvalidate = res.validate
    }).catch((response) => {
      this.$message.error('验证失败')
    })
  }
}
</script>

<style scoped>
    .validate-font{
        color: #495060;
        font-size: 40px;
        font-weight: bold;
        font-family: Helvetica Neue;
    }
</style>
