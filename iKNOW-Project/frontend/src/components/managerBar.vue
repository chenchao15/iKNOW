<!--导航栏 navigationBar-->
<template>
  <div class="tags">
    <img class='image' src="../assets/logo6.png"/>
    <a href="#/home" class="iKNOWlogo">iKNOW</a>
    <div v-if="quit === 1">
      <Button type="text" class="btn" style="right:100px;font-size:18px;font-weight: 500" @click="MouseClick()">退出</Button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'navigationBar',
  data () {
    return {
      quit: 0
    }
  },
  created () {
    if (this.$route.path === '/admin') {
      this.quit = 1
    }
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/admin' && from.path === '/adminlogin') {
        this.quit = 1
      }
      if (to.path === '/adminlogin' && from.path === '/admin') {
        this.quit = 0
      }
    }
  },
  methods: {
    MouseClick () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/logout')
        .then((response) => {
          this.$router.push('/adminlogin')
        })
        .catch((response) => {
          this.$Notice.error({
            title: '登出失败',
            desc: '管理员未登录'
          })
        })
    }
  }
}
</script>

<style>
    .tags{
        position: fixed; 
        top: 0; 
        left: 0; 
        width: 100%; 
        height: 50px; 
        background: #f8f8f9;
        z-index: 5;
    }
    .signup{
        position: fixed;
        top: 10px;
        right: 150px;
    }
    .image{
        position: absolute; 
        top: 0;
        left: 20px;
        height: 50px;
        width: 50px;
    }
    .iKNOWlogo{
        position: absolute;
        top: 0px;
        left: 75px;
        color: #495060;
        font-size: 30px;
        font-weight: bold;
        font-style: italic;
        font-family: Helvetica Neue;
    }
    .btn{
        position: fixed;
        top: 5px;
        font-weight: bold;
    }
</style>
