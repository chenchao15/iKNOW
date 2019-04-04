<template>
  <div>
    <navigationBar></navigationBar>
    <div class="layout">
      <div class="layout-content">
        <Row>
          <Col span="5">
            <Menu class="sidebar" :theme="chooseTheme" :active-name="chooseSelect" width="auto" :open-names="['competition_manage','stage_manage']" @on-select="chooseMenu">
              <Submenu name="competition_manage">
               <template slot="title">比赛管理</template>
                <MenuItem name="compete_manage_basic">比赛基本信息</MenuItem>
                <MenuItem name="compete_manage_stage">阶段管理</MenuItem>
                <MenuItem name="compete_manage_sign">比赛报名设置</MenuItem>
                <MenuItem name="compete_manage_file">附件上传管理</MenuItem>
              </Submenu>
              <MenuItem name="notice_manage">公告管理</MenuItem>
              <MenuItem name="group_message_manage">通知管理</MenuItem>
              <Submenu name="stage_manage">
               <template slot="title">阶段管理</template>
                <MenuItem :name="stage.id" v-for="stage in stageList" :key="stage.name">{{stage.name}}</MenuItem>
              </Submenu>
            </Menu>
          </Col>
          <Col span="19">
            <div class="layout-content-main">
              <div v-if="sidebarMenu === 'compete_manage_basic'">
                <competeManageBasic></competeManageBasic>
              </div>
              <div v-else-if="sidebarMenu === 'compete_manage_stage'">
                <competeManageStage></competeManageStage>
              </div>
              <div v-else-if="sidebarMenu === 'compete_manage_sign'">
                <competeManageSign></competeManageSign>
              </div>
              <div v-else-if="sidebarMenu === 'compete_manage_file'">
                <competeManageFile></competeManageFile>
              </div>
              <div v-else-if="sidebarMenu === 'notice_manage'">
                <noticeManage></noticeManage>
              </div>
              <div v-else-if="sidebarMenu === 'group_message_manage'">
                <groupMessageManage></groupMessageManage>
              </div>
              <div v-else>
                <stageManage :stageId="this.sidebarMenu"></stageManage>
              </div>
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
import noticeManage from '../components/noticeManage'
import groupMessageManage from '../components/groupMessageManage'
import competeManageBasic from '../components/competeManageBasic'
import competeManageStage from '../components/competeManageStage'
import competeManageSign from '../components/competeManageSign'
import competeManageFile from '../components/competeManageFile'
import stageManage from '../components/stageManage'

export default {
  name: 'CompetitionManage',
  data () {
    return {
      chooseTheme: 'light',
      sidebarMenu: 'compete_manage_basic',
      chooseSelect: 'compete_manage_basic',
      stageList: []
    }
  },
  components: {
    navigationBar,
    noticeManage,
    groupMessageManage,
    competeManageBasic,
    competeManageStage,
    competeManageSign,
    competeManageFile,
    stageManage
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/competitionmanage/' + this.$route.params.id) {
        this.sidebarMenu = 'compete_manage_basic'
        this.chooseSelect = 'compete_manage_basic'
      }
    }
  },
  mounted () {
    this.links()
  },
  methods: {
    links () { // 比赛id: this.$route.params.id
      var res = []
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/list_phase_simple?id=' + this.$route.params.id)
          .then((response) => {
            var res0 = JSON.parse(response.bodyText)
            res = res0
            this.stageList = res
          }).catch((response) => {
          })
    },
    chooseMenu: function (name) {
      this.GLOBAL.competitionType = name
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
        margin: 20px 100px 20px 20px;
        padding: 10px 25px 20px 20px;
    }
    .layout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
</style>
