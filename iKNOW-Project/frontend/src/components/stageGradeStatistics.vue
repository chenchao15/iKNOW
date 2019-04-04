<template>
<div>
  <div v-if="haveDataFlag === true">
    <div style="margin-top:20px;">
      <!--<Row class="playermanage-row">
        <Col span="2">
          <p style="margin-top:3px">选手类型</p>
        </Col>
        <Col span="4">
          <Select v-model="playerType" style="margin-left:10px">
            <Option v-for="(status, index) in competitionStatus" :value=status :key=status>{{status}}</Option>
          </Select> 
        </Col>
        <Col span="2" offset="1">
          <p style="margin-top:3px">筛选条件</p>
        </Col>
        <Col span="4">
          <Select v-model="selectCondition" style="margin-left:10px" @on-change="selectConditionChange">
            <Option v-for="(status, index) in conditions" :value=status :key=status>{{status}}</Option>
          </Select>
        </Col>
        <div v-if="selectPeopleFlag === true">
          <Col span="1" style="margin-left:20px">
            <Icon type="ios-arrow-thin-right" size="30" color="#aaa"></Icon>
          </Col>
          <Col span="4">
            <Input v-model="selectPeople" placeholder="输入搜索的名称…"></Input>
          </Col>
        </div>
        <Col span="4">
          <Button type="success" style="font-size:15px;margin-left:30px" @click="filterPlayers">点击筛选</Button>
        </Col>
      </Row>-->
      <Table :columns="tableColumns" :data="tableData"></Table>
      <div style="margin: 10px;overflow: hidden">
        <div style="float: right;">
          <Page :total="this.pageNum" :current="1" show-elevator @on-change="changePage"></Page>
        </div>
      </div>
    </div>
  </div>
  <Modal v-model="modifyflag" width="300" @on-ok="ismodify" style="text-align:center;">
    <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
      <Icon type="information-circled"></Icon>
      <span>修改成绩</span>
    </p>
    <p v-if="competitionType === '个人赛'" style="margin-bottom:10px; text-align:center">
      <span>姓名：{{modifyname}}</span>
    </p>
    <p v-else-if="competitionType === '小组赛'" style="margin-bottom:10px; text-align:center">
      <span>队伍：{{modifyname}}</span>
    </p>
    <p style="margin-bottom:10px; text-align:center">
      <span>原成绩：{{modifygrade}}</span>
    </p>
    新成绩：
    <InputNumber v-model="modifycontent" :min="0" style="width:100px"></InputNumber>
  </Modal>
</div>
</template>
<script>
  import gradeChildRow from '../components/grade-child-row.vue'
  export default {
    name: 'stageGradeStatistics',
    props: ['stageId'],
    data () {
      return {
        currentPage: 1,
        pageSize: 10,
        haveDataFlag: false,
        competitionType: null,
        competitionStage: '初赛',
        competition: { title: '2017年APMCM亚太地区大学生数学建模竞赛赛', stage: '初赛', type: '小组赛', id: 1 },
        pageNum: 0,
        modifyflag: false,
        modifycontent: 0,
        modifyindex: null,
        modifyname: null,
        modifygrade: null,
        tableData: [],
        selectPeopleFlag: false,
        selectPeople: null,
        playerType: '全部',
        selectCondition: '全部',
        conditions: ['全部', '成绩正序', '成绩逆序', '时间正序', '时间逆序', '筛选个人', '其它'],
        competitionStatus: ['全部', '初赛', '复赛', '决赛'],
        tableColumns: [
          {
            type: 'expand',
            width: 50,
            render: (h, params) => {
              return h(gradeChildRow, {
                props: {
                  row: params.row
                }
              })
            }
          },
          {
            title: '姓名',
            key: 'name',
            align: 'center',
            ellipsis: 'true'
          },
          {
            title: '操作',
            key: 'action',
            width: 250,
            align: 'center',
            render: (h, params) => {
              if (this.competitionType === '个人赛') {
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
                        this.show(params.index)
                      }
                    }
                  }, '成绩信息')
                  /* h('Button', {
                    props: {
                      type: 'success',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.modifyindex = params.index
                        this.modifyname = this.tableData[params.index].name
                        this.modifygrade = this.tableData[params.index].grade
                        this.gradeModify(params.index)
                      }
                    }
                  }, '成绩修改') */
                ])
              } else {
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
                        this.show(params.index)
                      }
                    }
                  }, '成绩信息')
                  /* h('Button', {
                    props: {
                      type: 'success',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.modifyindex = params.index
                        this.modifyname = this.tableData[params.index].name
                        this.modifygrade = this.tableData[params.index].grade
                        this.gradeModify(params.index)
                      }
                    }
                  }, '成绩修改') */
                ])
              }
            }
          }
        ]
      }
    },
    components: {
    },
    mounted () {
      this.haveDataFlag = true
      this.competitionType = this.competition.type
      if (this.competitionType === '个人赛') {
        this.conditions = ['全部', '成绩正序', '成绩逆序', '时间正序', '时间逆序', '筛选个人', '其它']
      } else {
        this.conditions = ['全部', '成绩正序', '成绩逆序', '时间正序', '时间逆序', '筛选队伍', '其它']
      }
      var dataGet = {
        phase_id: this.stageId,
        grade_type: 2
      }
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/grade_number', {params: dataGet})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.pageNum = res.joiner_number
      })
      .catch((response) => {
        this.$Message.error('获取成绩列表失败')
        this.pageNum = 0
      })
      this.links()
    },
    methods: {
      links () {
        /*   格式
        let data = []
        for (let i = 1; i <= 10; i++) {
          var num = 3 + Math.floor(Math.random() * 3)
          var submits = []
          for (let j = 1; j <= num; j++) {
            submits.push({
              submit_id: j,
              grade: Math.floor(Math.random() * 100),
              submit_time: new Date()
            })
          }
          data.push({
            name: 'people' + Math.floor(Math.random() * 100 + 1),
            submit_num: num,
            submit_history: submits
          })
        }
        */
        var dataGet = {
          phase_id: this.stageId,
          current_page: this.currentPage,
          grade_num: this.pageSize,
          grade_type: 2
        }
        this.$http.get(this.GLOBAL.baseUrl + 'api/competition/grade', {params: dataGet})
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.tableData = res.joiners
        })
        .catch((response) => {
          this.$Message.error('获取成绩列表失败')
          this.tableData = []
        })
      },
      formatDate (date) {
        const y = date.getFullYear()
        let m = date.getMonth() + 1
        m = m < 10 ? '0' + m : m
        let d = date.getDate()
        d = d < 10 ? ('0' + d) : d
        return y + '-' + m + '-' + d
      },
      changePage (count) {
        this.currentPage = count
        this.links()
      },
      show (index) {
        if (this.competitionType === '个人赛') {
          this.$Modal.info({
            title: '个人信息',
            content: `姓名：${this.tableData[index].name}<br>提交次数：${this.tableData[index].submit_num}`
          })
        } else {
          this.$Modal.info({
            title: '队伍信息',
            content: `队伍：${this.tableData[index].name}<br>成绩：${this.tableData[index].grade}<br>更新时间：${this.formatDate(this.tableData[index].update_time)}`
          })
        }
      },
      /* gradeModify (index) {
        this.modifyflag = true
      },
      ismodify () {
        this.modifyflag = false
        this.$Notice.success({
          title: '成绩已修改',
          desc: `“${this.tableData[this.modifyindex].name}”的成绩已被您修改<br>原成绩：${this.modifygrade}<br>修改后成绩：${this.modifycontent}`
        })
      }, */
      selectConditionChange (value) {
        if (value === '筛选个人' || value === '筛选队伍') {
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
        } else if (this.selectCondition === '筛选个人' || this.selectCondition === '筛选队伍') {
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
      }
    }
  }
</script>

<style scoped>
  .playermanage-row{
    font-size: 15px;
    margin-top: 10px;
    margin-bottom:10px;
  }
  .havedata-div{
    margin: 50px 0 20px 100px;
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

