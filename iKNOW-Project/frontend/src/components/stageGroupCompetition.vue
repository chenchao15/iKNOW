<template>
<div>
  <Row class="playermanage-row">
    <!--<Col span="2">
      <p style="margin-top:3px">选手类型</p>
    </Col>
    <Col span="2">
      <Select v-model="playerType" style="margin-left:10px">
        <Option v-for="(status, index) in competitionStatus" :value=status :key=status>{{status}}</Option>
      </Select> 
    </Col>
    <Col span="2" offset="1">
      <p style="margin-top:3px">筛选条件</p>
    </Col>
    <Col span="3">
      <Select v-model="selectCondition" style="margin-left:10px" @on-change="selectConditionChange">
        <Option v-for="(status, index) in conditions" :value=status :key=status>{{status}}</Option>
      </Select>
    </Col>
    <div v-if="selectPeopleFlag === true">
      <Col span="1" style="margin-left:20px">
        <Icon type="ios-arrow-thin-right" size="30" color="#aaa"></Icon>
      </Col>
      <Col span="3">
        <Input v-model="selectPeople" placeholder="输入队伍名字…"></Input>
      </Col>
    </div>
    <Col span="3">
      <Button type="success" style="font-size:15px;margin-left:30px" @click="filterPlayers">点击筛选</Button>
    </Col>-->
    <Col style="float: right;">
      <Button type="primary" style="font-size:15px;margin-left:30px" @click="importData">导入参赛者数据</Button>
    </Col>
  </Row>
  <Row>
    <div v-if="importFlag === true" class="candidate-style">
      <candidate v-on:message="recieveMessage"></candidate>
    </div>
  </Row>
  <Table :columns="teamColumns" :data="tableData"></Table>
  <div style="margin: 10px;overflow: hidden">
    <div style="float: right;">
      <Page :total="this.pageNum" :current="1" show-elevator @on-change="changePage"></Page>
    </div>
  </div>
  <Modal v-model="teampunishflag" width="300">
    <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
      <Icon type="information-circled"></Icon>
      <span>队伍处置</span>
    </p>
    <div style="text-align: center">
      <Button type="primary" @click="teamwarn">警告</Button>
      <!--<Button type="primary" @click="kickout">踢出</Button>-->
    </div>
  </Modal>
  <Modal v-model="teamwarnflag" width="300" @on-ok="isteamwarn">
    <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
      <Icon type="information-circled"></Icon>
      <span>警告队伍</span>
    </p>
    <p style="margin-bottom:10px; text-align:center">
      <span>警告队伍：{{teampunishname}}</span>
    </p>
    <Input v-model="warncontent" type="textarea" :autosize="{minRows: 2,maxRows: 6}" placeholder="请输入警告内容…"></Input>
  </Modal>
</div>
</template>
<script>
  import teamChildRow from '../components/team-child-row.vue'
  import candidate from '../components/candidate'
  export default {
    name: 'stageGroupCompetition',
    props: ['stageId'],
    data () {
      return {
        currentPage: 1,
        pageSize: 10,
        importFlag: false,
        chosenData: null,
        pageNum: 0,
        tableData: [],
        warncontent: null,
        selectPeopleFlag: false,
        selectPeople: null,
        teampunishflag: null,
        teamwarnflag: null,
        teampunishindex: null,
        teampunishname: null,
        playerType: '全部',
        selectCondition: '全部',
        conditions: ['全部', '成绩正序', '成绩逆序', '时间正序', '时间逆序', '筛选队伍', '其它'],
        competitionStatus: ['全部', '初赛', '复赛', '决赛'],
        competition: { title: '2017年APMCM亚太地区大学生数学建模竞赛赛', stage: '初赛', type: '小组赛', id: 1 },
        teamColumns: [
          {
            type: 'expand',
            width: 50,
            render: (h, params) => {
              return h(teamChildRow, {
                props: {
                  row: params.row
                }
              })
            }
          },
          {
            title: '队伍',
            key: 'team_name',
            align: 'center',
            render: (h, params) => {
              return h('div', this.tableData[params.index].team.name)
            }
          },
          {
            title: '队长',
            key: 'team_leader',
            align: 'center',
            render: (h, params) => {
              return h('div', this.tableData[params.index].leader.name)
            }
          },
          {
            title: '队员人数',
            key: 'team_number',
            align: 'center',
            render: (h, params) => {
              return h('div', this.tableData[params.index].team_number)
            }
          },
          {
            title: '操作',
            key: 'action',
            width: 200,
            align: 'center',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.team_show(params.index)
                    }
                  }
                }, '队伍详情'),
                h('Button', {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.teampunishindex = params.index
                      this.teampunishname = this.tableData[params.index].team_name
                      this.team_punish(params.index)
                    }
                  }
                }, '队伍处置')
              ])
            }
          }
        ]
      }
    },
    components: {
      teamChildRow,
      candidate
    },
    mounted () {
      var dataGet = {
        phase_id: this.stageId
      }
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/joiner_number', {params: dataGet})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.pageNum = res.joiner_number
      })
      .catch((response) => {
        this.$Message.error('获取参赛者列表失败')
        this.pageNum = 0
      })
      this.links()
    },
    methods: {
      links () {
        var dataGet = {
          phase_id: this.stageId,
          current_page: this.currentPage,
          joiner_num: this.pageSize
        }
        this.$http.get(this.GLOBAL.baseUrl + 'api/competition/joiner', {params: dataGet})
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.tableData = res.joiners
        })
        .catch((response) => {
          this.$Message.error('获取参赛者列表失败')
          this.tableData = []
        })
      },
      selectConditionChange (value) {
        if (value === '筛选队伍') {
          this.selectPeopleFlag = true
        } else {
          this.selectPeopleFlag = false
        }
      },
      filterPlayers () {
        var selectType = this.playerType === '初赛' ? 0 : this.playerType === '复赛' ? 1 : this.playerType === '决赛' ? 2 : 3
        let firstData = []
        let allData = []      // 从后端获取的所有数据
        if (selectType >= 0 && selectType <= 2) {
          for (var i in allData) {
            if (allData[i].type === selectType) {
              firstData.push(allData[i])
            }
          }
        } else {
          firstData = allData
        }
        if (this.selectCondition === '成绩正序') {
          firstData.sort(function (peoplea, peopleb) {
            return peopleb.grade - peoplea.grade
          })
        } else if (this.selectCondition === '成绩逆序') {
          firstData.sort(function (peoplea, peopleb) {
            return peoplea.grade - peopleb.grade
          })
        } else if (this.selectCondition === '时间正序') {
          firstData.sort(function (peoplea, peopleb) {
            return peopleb.time - peoplea.time
          })
        } else if (this.selectCondition === '时间逆序') {
          firstData.sort(function (peoplea, peopleb) {
            return peoplea.time - peopleb.time
          })
        } else if (this.selectCondition === '筛选队伍') {
          var flag = false
          for (var k in firstData) {
            if (firstData[k].name === this.selectPeople) {
              firstData = firstData[k]
              flag = true
              break
            }
          }
          if (!flag) {
            firstData = []
          }
        }
        this.tableData = firstData
      },
      changePage (count) {
        this.currentPage = count
        this.links()
      },
      team_show (index) {
        this.$Modal.info({
          title: '队伍信息',
          content: `队伍：${this.tableData[index].team.name}<br>队长：${this.tableData[index].leader.name}<br>队员人数：${this.tableData[index].team_number}`
        })
      },
      team_punish (index) {
        this.teampunishflag = true
      },
      teamwarn () {
        this.teampunishflag = false
        this.teamwarnflag = true
      },
      isteamwarn () {
        var dataPost = {
          phase_id: this.stageId,
          contestant_id: this.tableData[this.punishindex].leader.id,
          event_type: 7,
          is_team: 1,
          content: this.warncontent
        }
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/event', dataPost)
        .then((response) => {
          this.$Notice.success({
            title: '警告已发出',
            desc: `“${this.tableData[this.teampunishindex].team.name}”已被您警告<br>警告内容：${this.warncontent}`
          })
        })
        .catch((response) => {
          this.$Message.error('发送警告失败')
        })
      },
      show (index) {
        this.$Modal.info({
          title: '个人信息',
          content: `姓名：${this.tableData[index].leader.name}`
        })
      },
      importData () {
        if (this.importFlag) {
          this.importFlag = false
        } else {
          this.importFlag = true
        }
      },
      recieveMessage (msg) {
        this.importFlag = false
        this.chosenData = msg
      },
      reinit () {
        this.importFlag = false
        this.chosenData = null
        this.pageNum = 0
        this.tableData = []
        this.warncontent = null
        this.selectPeopleFlag = false
        this.selectPeople = null
        this.teampunishflag = null
        this.teamwarnflag = null
        this.teampunishindex = null
        this.teampunishname = null
      }
    }
  }
</script>

<style scoped>
  .playermanage-row{
    font-size: 15px;
    margin-top: 10px;
    margin-bottom:10px;
    text-align: center;
  }
  .havedata-div{
    margin: 50px 0 20px 300px;
    text-align: center;
  }
  .button-import{
    padding: 10px;
    font-size: 25px;
    text-align: center;
  }
  .candidate-style{
    margin-left: 70px;
    margin-bottom: 20px;
    text-align: center;
  }
</style>

