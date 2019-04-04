<template>
  <div>
    <navigationBar></navigationBar>
    <div class="layout">
      <div class="layout-content">
        <Row>
          <Col span="5">
            <Menu class="sidebar" :theme="chooseTheme" :active-name="chooseSelect" width="auto" :open-names="['competition', 'tutorial']" @on-select="chooseMenu">
              <MenuItem name="priinfo"><Icon type="person"></Icon>个人信息</MenuItem>
              <Submenu name="competition">
                <template slot="title">
                  <Icon type="ios-flag"></Icon>
                  比赛信息
                </template>
                <MenuItem name="joinCompetition">我参加的比赛</MenuItem>
                <MenuItem name="collectCompetition">我收藏的比赛</MenuItem>
              </Submenu>   
              <Submenu name="tutorial">
                <template slot="title">
                  <Icon type="ios-paper"></Icon>
                  教程信息
                </template>
                <MenuItem name="collectTutorial">我收藏的教程</MenuItem>
                <MenuItem name="postTutorial">我发布的教程</MenuItem>
                <MenuItem name="saveTutorial">我暂存的教程</MenuItem>
              </Submenu>
              <MenuItem name="primsg"><Icon type="ios-email"></Icon>私信</MenuItem>
            </Menu>
          </Col>
          <Col span="19">
            <div class="layout-content-main">
              <div v-if="sidebarMenu === 'priinfo'"><priinfo></priinfo></div>
              <div v-else-if="sidebarMenu === 'joinCompetition'"><joinCompetition></joinCompetition></div>
              <div v-else-if="sidebarMenu === 'collectCompetition'"><collectCompetition></collectCompetition></div>
              <div v-else-if="sidebarMenu === 'collectTutorial'"><collectTutorial></collectTutorial></div>
              <div v-else-if="sidebarMenu === 'postTutorial'"><postTutorial></postTutorial></div>
              <div v-else-if="sidebarMenu === 'saveTutorial'"><saveTutorial></saveTutorial></div>
              <div v-else-if="sidebarMenu === 'primsg'"><primsg></primsg></div>
            </div>
          </Col>
        </Row>
      </div>
      <div class="layout-copy">
        2011-2017 &copy; iKNOW
      </div>
    </div>
  </div>
</template>
<script>
import navigationBar from '../components/navigationBar'
import priinfo from '../components/priinfo'
import joinCompetition from '../components/prijoinCompetition'
import collectCompetition from '../components/pricollectCompetition'
import collectTutorial from '../components/pricollectTutorial'
import postTutorial from '../components/pripostTutorial'
import saveTutorial from '../components/prisaveTutorial'
import primsg from '../components/primsg'
export default {
  name: 'OrgPage',
  data () {
    return {
      chooseTheme: 'light',
      sidebarMenu: 'priinfo',
      chooseSelect: 'priinfo'
    }
  },
  components: {
    navigationBar,
    priinfo,
    joinCompetition,
    collectCompetition,
    collectTutorial,
    postTutorial,
    saveTutorial,
    primsg
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/pripage') {
        this.sidebarMenu = 'priinfo'
        this.chooseSelect = 'priinfo'
      }
    }
  },
  methods: {
    chooseMenu: function (name) {
      this.sidebarMenu = name
      this.chooseSelect = name
    }
  }
}
</script>

<style scoped>
    .sidebar{
        background: #f8f8f9;
        z-index: 0;
    }
    .label{
        padding: 30px 20px 0px 40px;
        font-size:14px;
        font-weight:bold;
    }
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        margin-top: 2%;
    }
    .layout-logo{
        width: 100px;
        height: 30px;
        background: #5b6270;
        border-radius: 3px;
        float: left;
        position: relative;
        top: 15px;
        left: 20px;
    }
    .layout-nav{
        width: 420px;
        margin: 0 auto;
    }
    .layout-assistant{
        width: 300px;
        margin: 0 auto;
        height: inherit;
    }
    .layout-breadcrumb{
        padding: 10px 15px 0;
    }
    .layout-content{
        min-height: 100%;
        margin: 15px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
    }
    .layout-content-main{
        margin: 10px 100px 0px 100px;
        padding: 10px 25px 0 20px;
    }
    .layout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
</style>
