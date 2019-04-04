<template>
<div>
  <div v-if="haveDataFlag === true">
    <div style="margin-top:20px;">
      <Row v-if="checkflag === true" class="card-row">
        <!--<Card>
          <Row>
            <p class="check-title">
              批改提交试卷
            </p>
          </Row>
          <Row>
            <p v-if="competitionType === '个人赛'">
              <Col span="5" offset="7">姓名：{{checkname}}</Col><Col span="5">提交时间：{{checktime}}</Col>
            </p>
            <p v-else-if="competitionType === '小组赛'">
              <Col span="5" offset="7">队伍：{{checkname}}</Col><Col span="5">提交时间：{{checktime}}</Col>
            </p>
          </Row>
          </Card>-->
          <Card>
            <Row>
              <p class="check-title">批改提交试卷</p>
            </Row>
            <Row style="margin-left:0px">
              <span>下载试卷：</span>
              <a :href="tableData[checkindex].submit_url" download>{{tableData[checkindex].submit_url}}</a>
            </Row>
            <Row class="card-footer">
              批改成绩：<InputNumber v-model="checkcontent" :min="0" style="width:100px"></InputNumber>
              <div style="float:right">
                <Button type="primary" @click="confirmButton">确定</Button>
                <Col span="4"></Col>
                <Button type="ghost" @click="cancelButton" style="margin-left:6px">取消</Button>
              </div>
            </Row>
          </Card>
        </Card>
      </Row>
      <!--<Row v-else-if="checkflag === false" class="playermanage-row">
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
      <Table border :columns="tableColumns" :data="tableData"></Table>
      <div style="margin: 10px;overflow: hidden">
        <div style="float: right;">
          <Page :total="this.pageNum" :current="1" show-elevator @on-change="changePage"></Page>
        </div>
      </div>
    </div>
  </div>
</div>
</template>
<script>
  export default {
    name: 'stageGradeCheck',
    props: ['stageId'],
    data () {
      return {
        currentPage: 1,
        pageSize: 10,
        haveDataFlag: false,
        competitionType: null,
        competitionStage: '初赛',
        competition: { title: '2017年APMCM亚太地区大学生数学建模竞赛赛', stage: '初赛', type: '个人赛', id: 1 },
        pageNum: 0,

        checkflag: false,
        checkcontent: 0,
        checkindex: null,
        checkname: null,
        checktime: null,
        checkstatus: null,
        tableData: [],
        selectPeopleFlag: false,
        selectPeople: null,
        playerType: '全部',
        selectCondition: '全部',
        DownloadItem: [],
        conditions: ['全部', '成绩正序', '成绩逆序', '时间正序', '时间逆序', '筛选个人', '其它'],
        competitionStatus: ['全部', '初赛', '复赛', '决赛'],
        examinationPaper: {content: '这绝对是一张试卷！', view_url: 'https://bugeinikana.com/biulibiuli', download_url: 'https://download/biulibiuli'},
        tableColumns: [
          {
            title: '提交者',
            key: 'name',
            align: 'center',
            render: (h, params) => {
              return h('div', this.tableData[params.index].contestant.name)
            }
          },
          {
            title: '批改成绩',
            key: 'grade',
            align: 'center',
            render: (h, params) => {
              return h('div', this.tableData[params.index].submit_grade)
            }
          },
          {
            title: '提交时间',
            key: 'time',
            align: 'center',
            render: (h, params) => {
              return h('div', this.tableData[params.index].time)
            }
          },
          {
            title: '批改状态',
            key: 'status',
            align: 'center',
            render: (h, params) => {
              const row = params.row
              const color = row.is_handled === 1 ? 'green' : row.is_handled === 0 ? 'red' : 'black'
              const text = row.is_handled === 1 ? '已批改' : row.is_handled === 0 ? '未批改' : 'default'
              return h('strong', {
                style: {
                  color: color
                }
              }, text)
            }
          },
          {
            title: '操作',
            key: 'action',
            width: 250,
            align: 'center',
            render: (h, params) => {
              /* const mtype = this.checkflag === true ? 'success' : 'error'
              const text = this.checkflag === true ? '成绩批改中' : '成绩批改' */
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
                  }, '个人信息'),
                  h('Button', {
                    props: {
                      type: 'warning',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.checkindex = params.index
                        this.gradeCheck(params.index)
                      }
                    }
                  }, '成绩批改')
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
                  }, '队伍信息'),
                  h('Button', {
                    props: {
                      type: 'warning',
                      size: 'small'
                    },
                    on: {
                      click: () => {
                        this.checkindex = params.index
                        this.gradeCheck(params.index)
                      }
                    }
                  }, '成绩批改')
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
      /* var dataGet = {
        phase_id: this.stageId
      }
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/joiner_type', {params: dataGet})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.competitionType = res.joiner_type
      })
      .catch((response) => {
        this.$Message.error('获取参赛者类型失败')
        this.competitionType = 0
      }) */
      if (this.competitionType === '个人赛') {
        this.conditions = ['全部', '成绩正序', '成绩逆序', '时间正序', '时间逆序', '筛选个人', '其它']
      } else {
        this.conditions = ['全部', '成绩正序', '成绩逆序', '时间正序', '时间逆序', '筛选队伍', '其它']
        this.tableColumns[0].title = '提交队伍'
      }
      var dataGet = {
        phase_id: this.stageId,
        grade_type: 1
      }
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/grade_number', {params: dataGet})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.pageNum = res.grade_number
      })
      .catch((response) => {
        this.$Message.error('获取成绩列表失败')
        this.pageNum = 0
      })
      // 获取试卷格式get
      this.DownloadItem = [
        {name: '', type: 'singleLine', value: '请同学们在此处下载本阶段的试题'},
        {name: '大数据竞赛', type: 'Upload', value: '点击上传本阶段试题', fileUrl: ''}
      ]
      this.links()
    },
    methods: {
      links () {
        var dataGet = {
          phase_id: this.stageId,
          current_page: this.currentPage,
          grade_num: this.pageSize,
          grade_type: 1
        }
        this.$http.get(this.GLOBAL.baseUrl + 'api/competition/grade', {params: dataGet})
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.tableData = res
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
            content: `姓名：${this.tableData[index].name}`
          })
        } else {
          this.$Modal.info({
            title: '队伍信息',
            content: `队伍：${this.tableData[index].name}`
          })
        }
      },
      gradeCheck (index) {
        if (this.checkflag) {
          this.checkflag = false
        } else {
          this.checkflag = true
          this.checkstatus = this.tableData[this.checkindex].status
          this.tableData[this.checkindex].status = 3
        }
      },
      confirmButton () {
        this.checkflag = false
        var dataPost = {
          grade_id: this.tableData[this.checkindex].id,
          submit_grade: this.checkcontent
        }
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/handle_grade', dataPost)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.tableData[this.checkindex].is_handled = 1
          this.tableData[this.checkindex].submit_grade = res.submit_grade
          this.$Notice.success({
            title: '成绩已批改',
            desc: `“${this.tableData[this.checkindex].contestant.name}”的成绩已批改完成<br>批改成绩：${this.tableData[this.checkindex].submit_grade}`
          })
        })
        .catch((response) => {
          this.$Message.error('成绩批改失败')
        })
        this.checkcontent = 0
      },
      cancelButton () {
        this.checkflag = false
        this.checkcontent = 0
      },
      selectConditionChange (value) {
        if (value === '筛选个人' || value === '筛选队伍') {
          this.selectPeopleFlag = true
        } else {
          this.selectPeopleFlag = false
        }
      },
      viewPaper (viewUrl) {
        this.$router.push(viewUrl)
      },
      downloadPaper (downloadUrl) {
        this.$router.push(downloadUrl)
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
  .card-row{
    margin: 20px 0;
    text-align: center;
  }
  .card-content{
    margin: 20px 0;
    text-align: center;
  }
  .card-footer{
    margin-top: 20px;
    margin-left: 100px;
    text-align: center;
  }
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
  .check-title{
    margin-bottom: 10px;
    text-align: center;
    font-size: 20px;
    font-color: black;
    font-weight: bold;
  }
  .TestUpload-p{
    margin-top: 3px;
    font-weight: normal;
  }
  .upload-card{
    margin-top: 20px; 
    text-align: left;
    font-weight: bold;
  }
</style>

