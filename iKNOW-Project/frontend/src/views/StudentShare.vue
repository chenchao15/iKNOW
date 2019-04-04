<template>
<div>
  <navigationBar></navigationBar>
  <div class="layout">
    <div class="layout-content">
      <div class="layout-content-main">
        <Row>
          <Col span="3">
            <p class="tutorial-title">学友分享</p>
          </Col>
          <Col v-if="this.isLogin == 1 && this.isType == 0" span="3" offset="16">
            <Button class="share-button" type="text" size="large" @click="goShare">我要分享<Icon type="android-share"></Icon></Button>
          </Col>
        </Row>
        <Row>
          <hr color="#bbbec4" size="2" />
        </Row>
        <Row class="tutorial-content">
          <Tabs value="allTutorial">
            <TabPane class="tutorial-tabpane" label="全部教程" name="allTutorial">
              <studentShareCard type="0"></studentShareCard>
            </TabPane>
            <TabPane class="tutorial-tabpane" label="最新发布" name="latestRelease">
              <studentShareCard type="1"></studentShareCard>
            </TabPane>
            <TabPane class="tutorial-tabpane" label="最多推荐" name="mostRecommend">
              <studentShareCard type="2"></studentShareCard>
            </TabPane>
          </Tabs>
        </Row>
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
import studentShareCard from '../components/studentShareCard'
export default {
  name: 'OfficialTutorial',
  data () {
    return {
      isLogin: 0,
      isType: -1,
      currentShare: {
        title: '',
        content: '',
        author: {
          id: 1,
          name: 'fddf',
          avatar_url: ''
        },
        brief: '',
        createTime: '',
        id: -1
      }
    }
  },
  components: {
    navigationBar,
    studentShareCard
  },
  created () {
    this.getCookie()
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/studentShare') {
        this.getCookie()
      }
    }
  },
  methods: {
    getCookie () {
      if (document.cookie.length > 0) {
        var arr = document.cookie.split('; ')
        for (var i = 0; i < arr.length; i++) {
          var arr2 = arr[i].split('=')
          if (arr2[0] === 'islogin') {
            this.isLogin = arr2[1]
          } else if (arr2[0] === 'usertype') {
            this.isType = arr2[1]
          }
        }
      }
    },
    goShare () {
      this.$router.push('/createtutorial')
    }
  }
}
</script>

<style scoped>
    .tutorial-title{
        margin: 10px;
        text-align: center;
        display: inline-block;
        font-size: 25px;
        color: #666;
        font-weight: 600;
        overflow: hidden;
    }
    .share-button{
        margin: 10px;
        margin-left: 80px;
        text-align:center;
        display: inline-block;
        font-family: "PingFang SC";
        font-size: 18px;
        overflow: hidden;
    }
    .tutorial-content{
        margin: 20px 50px;
        z-index: 0;
    }
    .tutorial-tabpane{
        margin-top: -15px;
        padding: 0px 60px;
    }
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
    }
    .layout-content{
        min-height: 200px;
        margin: 15px;
        padding: 50px;
        padding-top: 10px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
    }
    .layout-content-main{
        padding: 10px;
    }
    .layout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
</style>
