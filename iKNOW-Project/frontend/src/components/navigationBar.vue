<template>
  <div class="tags">
    <img class='image' src="../assets/logo6.png"/>
    <a href="#/home" class="iKNOWlogo">iKNOW</a>
    <Button type="text" class="btn" style="left:200px;font-size:18px;font-weight: 500" @click="MouseClick(1)">首页</Button>
    <Button type="text" class="btn" style="left:250px;font-size:18px;font-weight: 500" @click="MouseClick(2)">比赛</Button>
    <Button type="text" class="btn" style="left:300px;font-size:18px;font-weight: 500" @click="MouseClick(4)">官方教程</Button>
    <Button type="text" class="btn" style="left:390px;font-size:18px;font-weight: 500" @click="MouseClick(5)">学友分享</Button>
    <div v-if="isLogin == 0">
      <Button type="text" class="btn" style="padding: 6px 0;right:100px;font-size:18px;font-weight: 500" @click="MouseClick(6)">注册</Button>
      <Button type="text" class="btn" style="padding: 6px 0;right:60px;font-size:18px;font-weight: 500" @click="MouseClick(7)">登录</Button>
    </div>
    <div v-else-if="isLogin == 1">
      <Dropdown trigger="click" @on-click="mouse" class="dropdown">
        <Avatar icon="person" size="large" class="ava" v-if="this.avatarUrl === 'static/img/avatar/default_avatar.png'"/>
        <Avatar :src="this.avatarUrl" size="large" class="ava" v-if="this.avatarUrl !== 'static/img/avatar/default_avatar.png'"/>
        <br/><br/>
        <DropdownMenu slot="list">
          <DropdownItem name="orgmsg" v-if="isType == 1">组织主页</DropdownItem>
          <DropdownItem name="primsg" v-if="isType == 0">个人主页</DropdownItem>
          <DropdownItem name="create" v-if="isType == 1">创建比赛</DropdownItem>
          <DropdownItem name="quit" divided>退出登录</DropdownItem>
        </DropdownMenu>
      </Dropdown>
    </div>
    <Input v-model="searchValue" placeholder="搜索..." style="width:350px;left:660px;top:10px">
      <Select v-model="selectOption" slot="prepend" style="width:70px">
        <Option value="0">比赛</Option>
        <Option value="1">组织</Option>
        <Option value="2">教程</Option>
      </Select>
      <Button slot="append" icon="ios-search" @click="search"></Button>
    </Input>
  </div>
</template>

<script>
export default {
  name: 'navigationBar',
  data () {
    return {
      avatarUrl: this.GLOBAL.avatarUrl,
      searchValue: '',
      selectOption: '0',
      isLogin: this.GLOBAL.islogin,
      isType: this.GLOBAL.userType
    }
  },
  watch: {
    '$route': 'getLoginStatusCookie'
  },
  mounted () {
    this.getLoginStatusCookie()
  },
  methods: {
    // 读取登录状态cookie
    getLoginStatusCookie () {
      if (document.cookie.length > 0) {
        var tempid = -1
        var arr = document.cookie.split('; ')
        for (var i = 0; i < arr.length; i++) {
          var arr2 = arr[i].split('=')
          if (arr2[0] === 'islogin') {
            this.isLogin = arr2[1]
            this.GLOBAL.islogin = arr2[1]
          } else if (arr2[0] === 'usertype') {
            this.isType = arr2[1]
            this.GLOBAL.userType = arr2[1]
          } else if (arr2[0] === 'userid') {
            tempid = arr2[1]
          } else if (arr2[0] === 'avatarurl') {
            this.avatarUrl = arr2[1]
            this.GLOBAL.avatarUrl = arr2[1]
          }
        }
        if (this.isType === 0) {
          this.GLOBAL.priUserId = tempid
        } else if (this.isType === 1) {
          this.GLOBAL.orgUserId = tempid
        }
        // this.ischecked = 0 // 0未审核 1待审核 2已审核通过
      }
    },
    // 清除登录状态cookie
    clearLoginStatusCookie () {
      var exdate = new Date() // 获取时间
      exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * 7) // 保存的天数
      this.GLOBAL.islogin = 0
      window.document.cookie = 'islogin=' + 0 + ';path=/;expires=' + exdate.toGMTString()
      this.GLOBAL.userType = -1
      window.document.cookie = 'usertype=' + -1 + ';path=/;expires=' + exdate.toGMTString()
      window.document.cookie = 'userid=' + -1 + ';path=/;expires=' + exdate.toGMTString()
      window.document.cookie = 'avatarurl=' + '' + ';path=/;expires=' + exdate.toGMTString()
    },
    MouseClick (n) {
      if (n === 1) {
        this.$router.push('/home')
      } else if (n === 2) {
        this.$router.push('/competitions')
      } else if (n === 3) {
        this.$router.push('/forum')
      } else if (n === 4) {
        this.$router.push('/officialTutorial')
      } else if (n === 5) {
        this.$router.push('/studentShare')
      } else if (n === 6) {
        this.$router.push('/signup')
      } else if (n === 7) {
        this.$router.push('/login')
      }
    },
    mouse: function (name) {
      if (name === 'orgmsg') {
        this.$router.push('/orgpage')
      } else if (name === 'primsg') {
        this.$router.push('/pripage')
      } else if (name === 'create') {
        this.$router.push('/createcompetition')
      } else if (name === 'manage') {
        this.$router.push('/competitionmanage')
      } else if (name === 'quit') {
        this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/logout')
        .then((response) => {
          this.isLogin = 0
          this.clearGlobal()
          this.clearLoginStatusCookie()
          this.$router.push('/home')
        })
        .catch((response) => {
          this.isLogin = 1
        })
      } else {
        this.$router.push('/login')
      }
    },
    search () {
      if (this.searchValue === '') {
        this.$Notice.error({
          title: '搜索失败',
          desc: '请输入搜索内容'
        })
      } else {
        this.$router.push('/search/' + this.selectOption + '/' + this.searchValue)
      }
    },
    clearGlobal () {
      this.GLOBAL.priUserId = -1
      this.GLOBAL.userType = -1
      this.GLOBAL.orgUserId = -1
      this.GLOBAL.curChatName = ''
      this.GLOBAL.curChatTime = ''
      this.GLOBAL.curChatContent = ''
      this.GLOBAL.orgInfoForm.name = ''
      this.GLOBAL.priInfoForm.name = ''
      this.GLOBAL.competitionType = -1
      this.GLOBAL.islogin = 0
      this.GLOBAL.avatarUrl = ''
      this.GLOBAL.competeBasicInfo.name = ''
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
    .login{
        position: fixed;
        top: 10px;
        right: 100px;
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
    .ava{
        float: right;
        margin-right: 25px;
    }
    .dropdown{
        float: right;
        margin-right: 50px;
        margin-top: 5px;
    }
</style>
