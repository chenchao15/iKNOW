<template>
<div>
  <navigationBar></navigationBar>
  <div class="layout">
    <div class="layout-content">
      <div class="layout-content-main">
        <Row>
          <Col span="3">
            <p class="tutorial-title">官方教程</p>
          </Col>
          <Col v-if="this.islogin == 1 && this.istype == 1" span="3" offset="16">
            <Button class="share-button" type="text" size="large" @click="goPublish">发布教程<Icon type="android-share"></Icon></Button>
          </Col>
        </Row>
        <Row>
          <hr color="#bbbec4" size="2" />
        </Row>
        <Row class="tutorial-content">
          <Tabs value="allTutorial">
            <TabPane class="tutorial-tabpane" label="全部教程" name="allTutorial">
              <officialTutorialCard type="0"></officialTutorialCard>
            </TabPane>
            <TabPane class="tutorial-tabpane" label="最新发布" name="latestRelease">
              <officialTutorialCard type="1"></officialTutorialCard>
            </TabPane>
            <TabPane class="tutorial-tabpane" label="最多推荐" name="mostRecommend">
              <officialTutorialCard type="2"></officialTutorialCard>
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
import officialTutorialCard from '../components/officialTutorialCard'
export default {
  name: 'OfficialTutorial',
  data () {
    return {
      islogin: 0,
      istype: -1,
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
    officialTutorialCard
  },
  created () {
    this.getCookie()
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/officialTutorial') {
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
            this.islogin = arr2[1]
          } else if (arr2[0] === 'usertype') {
            this.istype = arr2[1]
          }
        }
      }
    },
    goPublish () {
      this.$router.push('/createtutorial')
    }
  }
}
</script>

<style scoped>
    .tutorial-title{
        margin: 10px;
        text-align:center;
        display: inline-block;
        font-size: 25px;
        color: #666;
        font-weight: 600;
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
    .share-button{
        margin: 10px;
        margin-left: 80px;
        text-align:center;
        display: inline-block;
        font-family: "PingFang SC";
        font-size: 18px;
        overflow: hidden;
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
