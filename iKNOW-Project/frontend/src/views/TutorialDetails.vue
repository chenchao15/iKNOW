<template>
  <div>
    <navigationBar></navigationBar>
    <div class="layout">
      <div class="layout-content">
        <Row>
          <Col span="19">
            <h1>{{tutorial.title}}</h1>
          </Col>
          <Col v-if="isType == 0" span="2" offset="3">
            <Button type="text" :icon="heartCollect" @click="collect">{{isCollect}}</Button>
            <p style="color:#9ea7b4">已有{{tutorial.collect_number}}人收藏</p>
          </Col>
        </Row>
        <Row>
          <a @click="lookOtherPage()" v-if="this.type === 0">{{tutorial.author.contestant_user.name}}</a>
          <a @click="lookOtherPage()" v-if="this.type === 1">{{tutorial.author.organizer_user.name}}</a>
          <label style="color:#9ea7b4">{{tutorial.post_time}}</label>
        </Row>
        <hr style="color:#9ea7b4;margin:4px 0"/>
        <p style="font-size:15px" v-html="tutorial.content"></p>
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
  name: 'TutorialDetails',
  data () {
    return {
      heartCollect: 'ios-heart-outline',
      isCollect: '收藏',
      type: -1,
      isType: -1,
      tutorial: {}
    }
  },
  components: {
    navigationBar
  },
  created () {
    this.links()
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/tutorialDetails/' + this.$route.params.id) {
        this.links()
      }
    }
  },
  methods: {
    links () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/tutorial/tutorial_info/' + this.$route.params.id)
        .then((response) => {
          var res0 = JSON.parse(response.bodyText)
          this.tutorial = res0
          if (res0.author.contestant_user === null) {
            this.type = 1
          } else {
            this.type = 0
          }
        }).catch((response) => {
          this.$Message.error('失败')
        })
      this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/is_tutorial?tutorial_id=' + this.$route.params.id)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          if (res.tutorial_status === 0) {
            this.heartCollect = 'ios-heart-outline'
            this.isCollect = '收藏'
          } else {
            this.heartCollect = 'ios-heart'
            this.isCollect = '取消收藏'
          }
          this.collect_number = res.collect_number
        }).catch((response) => {
        })
      this.getLoginStatusCookie()
    },
    getLoginStatusCookie () {
      if (document.cookie.length > 0) {
        var arr = document.cookie.split('; ')
        for (var i = 0; i < arr.length; i++) {
          var arr2 = arr[i].split('=')
          if (arr2[0] === 'usertype') {
            this.isType = arr2[1]
          }
        }
      }
    },
    collect () {
      var dataPost
      if (this.heartCollect === 'ios-heart') {
        dataPost = {
          tutorial_id: this.$route.params.id,
          status: 0
        }
        this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/collect_tutorial', dataPost)
        .then((response) => {
          this.heartCollect = 'ios-heart-outline'
          this.isCollect = '收藏'
          this.tutorial.collect_number--
        })
        .catch((response) => {
        })
      } else {
        dataPost = {
          tutorial_id: this.$route.params.id,
          status: 1
        }
        this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/collect_tutorial', dataPost)
        .then((response) => {
          this.heartCollect = 'ios-heart'
          this.isCollect = '取消收藏'
          this.tutorial.collect_number++
        })
        .catch((response) => {
        })
      }
    },
    lookOtherPage () {
      var type = this.type
      var id = (type === 0 ? this.tutorial.author.contestant_user.id : this.tutorial.author.organizer_user.id)
      var mid = this.tutorial.author.id
      this.$router.push('/otherUserPage/' + mid + '/' + id + '/' + type)
    }
  }
}
</script>

<style scoped>
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        margin-top: 2%;
    }
    .layout-content{
        min-height: 100%;
        margin: 15px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
        padding:20px;
    }
    .layout-content-main{
        padding: 50px 200px 30px 200px;
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
