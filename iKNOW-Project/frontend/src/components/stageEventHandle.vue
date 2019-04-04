<template>
  <div class="eventHandle">
    <Row class="eventHandle-row">
      <Col span="2">
        <p style="margin-top:3px">事件类型</p>
      </Col>
      <Col span="8">
        <Select v-model="typeSelect" style="width:200px;margin-left:10px">
          <Option value=0 key="0">全部</Option>
          <Option v-if="stageType === 0" value=1 key="1">申请报名</Option>
          <Option v-if="stageType === 1" value=1 key="1">队长报名</Option>
          <Option value=2 key="2">申请退出</Option>
          <Option value=3 key="3">申诉</Option>
          <Option value=4 key="4">移交队长</Option>
          <Option value=5 key="5">申请队长</Option>
          <Option value=6 key="6">申请编辑资料</Option>
          <Option v-if="stageType === 1" value=8 key="8">队员报名</Option>
        </Select> 
      </Col>
      <Col span="2">
        <p style="margin-top:3px">事件状态</p>
      </Col>
      <Col span="7">
        <Select v-model="statusSelect" style="width:200px;margin-left:10px">
          <Option value=0 key="0">全部</Option>
          <Option value=1 key="1">未审核</Option>
          <Option value=2 key="2">已通过</Option>
          <Option value=3 key="3">未通过</Option>
        </Select>
      </Col>
      <Col span="4">
        <Button type="success" style="font-size:15px;margin-left:30px" @click="links(1)">点击筛选</Button>
      </Col>
    </Row>
    <Table :data="tableData" :columns="tableColumns1" stripe></Table>
    <Modal v-model="modifyModal" width="800">
      <p slot="header" style="color:#2d8cf0;text-align:center">
        <Icon type="information-circled"></Icon>
        <span>事件详情({{currentEvent.type}})</span>
      </p>
      <div class="eventHandle-modal">
        <div v-if="currentEvent.type === '申请报名' || currentEvent.type === '队长报名'">
          <div v-for="i in currentEvent.steps" :key="i.name">
            <strong>{{i.name}}</strong>
            <Row v-for="j in i.item" :key="j" style="margin-bottom: 5px">
              <Col span="5"><p style="font-size: 15px; font-weight:500;font-family: PingFang SC">{{j.name}}</p></Col>
              <Col span="19">
                <div v-if="j.type !== 'Upload'">
                  <span v-for="data in j.value" style="font-size: 16px; font-family: KaiTi;word-break:break-all; word-wrap:break-word">{{data}} </span>
                </div>
                <a v-if="j.type === 'Upload'" style="font-size: 16px; font-family: KaiTi;word-break:break-all; word-wrap:break-word" :href="j.value[0]" download>点击查看链接</a>
              </Col>
            </Row>
          </div> 
        </div>
        <div v-else-if="currentEvent.type === '队员报名' || currentEvent.type === '申请编辑资料'">
          <div v-for="(i, index) in currentEvent.steps" v-if="index > 0":key="i.name">
            <strong>{{i.name}}</strong>
            <Row v-for="j in i.item" :key="j" style="margin-bottom: 5px">
              <Col span="5"><p style="font-size: 15px; font-weight:500;font-family: PingFang SC">{{j.name}}</p></Col>
              <Col span="19">
                <div v-if="j.type !== 'Upload'">
                  <span v-for="data in j.value" style="font-size: 16px; font-family: KaiTi;word-break:break-all; word-wrap:break-word">{{data}} </span>
                </div>
                <a v-if="j.type === 'Upload'" style="font-size: 16px; font-family: KaiTi;word-break:break-all; word-wrap:break-word" :href="j.value[0]" download>点击查看链接</a>
              </Col>
            </Row>
          </div> 
        </div>
        <div v-else>
          <strong>申请理由</strong>
          <p style="font-size: 16px; font-family: KaiTi;word-break:break-all; word-wrap:break-word">{{currentEvent.steps}}</p>
        </div>
        <div style="margin-top: 20px">
          <Row>
            <Col span="3">
              <p style="color:red; font-size: 17px">审批理由</p>
            </Col>
            <Col span="20">
              <Input type="textarea" v-model="currentEvent.reason" :autosize="{minRows: 3,maxRows: 5}"></Input>
            </Col>
          </Row>
        </div>
      </div>
      <div slot="footer">
        <Button type="info" style="font-size: 16px" @click="linkPost(2)">通过并审核下一个</Button>
        <Button type="info" style="font-size: 16px" @click="linkPost(3)">拒绝并审核下一个</Button>
      </div>
    </Modal>
    <div style="margin: 10px;overflow: hidden">
        <div style="float: right;">
          <Page :total="this.pageNum" :current="this.proPage" @on-change="changePage" show-elevator></Page>
        </div>
    </div>
  </div>
</template>
<script>
  export default {
    props: ['stageId'],
    data () {
      return {
        stageType: -1,
        tableData: [],
        pageNum: 0,
        proPage: 1,
        eventNum: 10,
        modifyModal: false,
        currentEvent: {},
        signTable: [],
        typeSelect: '0',
        statusSelect: '0',
        tableColumns1: [
          {
            title: '事件发起人',
            key: 'name',
            align: 'center',
            render: (h, params) => {
              const text = params.row.contestant.user.contestant_user.name
              return h('p', {
                style: {
                  fontSize: '14px'
                }
              }, text)
            }
          },
          {
            title: '事件类型',
            key: 'status',
            width: 170,
            align: 'center',
            render: (h, params) => {
              const row = params.row
              const color = row.type === 1 ? 'green' : row.type === 2 ? 'default' : row.type === 3 ? 'red' : row.type === 6 ? 'yellow' : 'blue'
              const text = (row.type === 1 && this.stageType === 0) ? '申请报名' : (row.type === 1 && this.stageType === 1) ? '队长报名' : row.type === 2 ? '申请退出' : row.type === 3 ? '申诉' : row.type === 4 ? '申请移交队长' : row.type === 5 ? '申请队长' : row.type === 6 ? '申请编辑资料' : row.type === 8 ? '队员报名' : '其他'
              return h('Tag', {
                props: {
                  type: 'dot',
                  color: color
                }
              }, text)
            }
          },
          {
            title: '更新时间',
            key: 'time',
            width: 100,
            align: 'center',
            render: (h, params) => {
              return h('div', this.tableData[params.index].time)
            }
          },
          {
            title: '选项',
            key: 'action',
            width: 250,
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
                      this.showDetail(params.index)
                    }
                  }
                }, '审核查看'),
                h('Button', {
                  props: {
                    type: 'success',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.linkPassPost(params.index)
                    }
                  }
                }, '通过'),
                h('Button', {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.linkRejectPost(params.index)
                    }
                  }
                }, '拒绝')
              ])
            }
          },
          {
            title: '状态',
            key: 'status',
            align: 'center',
            render: (h, params) => {
              const row = params.row
              const color = row.status === 1 ? 'red' : row.status === 2 ? 'green' : 'black'
              const text = row.status === 2 ? '审核通过' : row.status === 3 ? '审核不通过' : '未审核'
              return h('strong', {
                style: {
                  color: color,
                  fontSize: '14px'
                }
              }, text)
            }
          }
        ]
      }
    },
    beforeCreate () {
      this.eventNum = 10
      this.proPage = 1
      this.typeSelect = '0'
      this.statusSelect = '0'
    },
    mounted () { // 当前阶段id: this.stageId
      var dataGet = {
        phase_id: this.stageId,
        event_type: Number(this.typeSelect),
        status: Number(this.statusSelect)
      }
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/event_number', {params: dataGet})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.pageNum = res.event_number
      })
      .catch((response) => {
        this.$Message.error('获取事件列表失败')
        this.pageNum = 0
      })
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/detailPhase/' + this.stageId)
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.signTable = JSON.parse(res.enrolment_method)
        var len = this.signTable.length
        for (var i = 0; i < len; i++) {
          this.signTable[i].item = JSON.parse(this.signTable[i].item)
        }
      })
      .catch((response) => {
      })
      this.links(0)
    },
    methods: { // 当前阶段id: this.stageId
      links (page) {
        if (page === 1) {
          this.proPage = 1
        }
        var dataGet = {
          phase_id: this.stageId,
          current_page: this.proPage,
          event_num: this.eventNum,
          event_type: Number(this.typeSelect),
          status: Number(this.statusSelect)
        }
        this.$http.get(this.GLOBAL.baseUrl + 'api/competition/event', {params: dataGet})
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          for (let i = 0; i < res.length; i++) {
            res[i].type = res[i].event_type
            res[i].items = []
            res[i].items.push(res[i].content)
          }
          if (res[0] === undefined) {
            this.tableData = []
          } else {
            this.tableData = res
          }
        })
        .catch((response) => {
          this.$Message.error('获取事件列表失败')
        })
        dataGet = {
          phase_id: this.stageId
        }
        this.$http.get(this.GLOBAL.baseUrl + 'api/competition/joiner_type', {params: dataGet})
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.stageType = res.joiner_type
          console.log(this.stageType)
        })
      },
      changePage (count) {
        this.proPage = count
        this.links(0)
      },
      showDetail (index) {
        this.modifyModal = true
        let arr = this.tableData[index]
        this.currentEvent = {
          id: arr.id,
          type: (arr.type === 1 && this.stageType === 0) ? '申请报名' : (arr.type === 1 && this.stageType === 1) ? '队长报名' : arr.type === 2 ? '申请退出' : arr.type === 3 ? '申诉' : arr.type === 4 ? '申请移交队长' : arr.type === 5 ? '申请队长' : arr.type === 6 ? '申请编辑资料' : arr.type === 8 ? '队员报名' : '其他',
          steps: '',
          next: index + 1,
          reason: arr.reason
        }
        if (arr.type === 1 || arr.type === 6 || arr.type === 8) {
          this.currentEvent.steps = this.signTable
          var len1 = this.currentEvent.steps.length
          var len2
          var data = JSON.parse(arr.items[0])
          let index = 0
          let i = 0
          let j = 0
          var k = 0
          if (arr.type === 8 || arr.type === 6) {
            k = 1
          }
          for (index = k; index < len1; index++) {
            len2 = this.currentEvent.steps[index].item.length
            for (i = 0; i < len2; i++) {
              this.currentEvent.steps[index].item[i].value = data[j]
              j++
            }
          }
          console.log(JSON.stringify(this.currentEvent.steps))
        } else {
          this.currentEvent.steps = arr.items[0]
        }
      },
      linkPost (status) {
        /* if (this.tableData[this.currentEvent.next - 1].status !== 1) {
          this.$Notice.error({
            title: '错误',
            desc: '您已经审核过该事件了'
          })
          return
        } */
        var data = {
          id: this.currentEvent.id,
          status: status,
          reason: this.currentEvent.reason
        }
        var name = this.tableData[this.currentEvent.next - 1].contestant.user.contestant_user.name
        var id = this.tableData[this.currentEvent.next - 1].contestant.user.id
        var content = ''
        if (status === 2) {
          content = '亲爱的＂' + name + '＂同学，你好，恭喜你已通过审核．审批结果如下：'
        } else {
          content = '亲爱的＂' + name + '＂同学，你好，很遗憾你没有通过审核．审批结果如下：'
        }
        content += data.reason
        this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/personal_letter', {id: id, content: content})
        .then((response) => {
        })
        .catch((response) => {
        })
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/handle_event', data)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.tableData[this.currentEvent.next - 1].status = Number(res.status)
          this.tableData[this.currentEvent.next - 1].reason = res.reason
          if (this.currentEvent.next < this.eventNum) {
            this.showDetail(this.currentEvent.next)
          } else {
            this.currentEvent.next = 0
            this.proPage++
            this.links(0)
            this.showDetail(this.currentEvent.next)
          }
        })
        .catch((response) => {
          this.$Message.error('您已经审核到最后一个了,可直接关闭窗口')
        })
      },
      linkPassPost (index) {
        /* if (this.tableData[index].status !== 1) {
          this.$Notice.error({
            title: '错误',
            desc: '您已经审核过该事件了'
          })
          return
        } */
        let arr = this.tableData[index]
        var data = {
          id: arr.id,
          status: 2,
          reason: arr.reason
        }
        var name = this.tableData[index].contestant.user.contestant_user.name
        var id = this.tableData[index].contestant.user.id
        var content = '亲爱的＂' + name + '＂同学，你好，恭喜你已通过审核．请及时查看比赛相关信息，准备比赛'
        this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/personal_letter', {id: id, content: content})
        .then((response) => {
        })
        .catch((response) => {
        })
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/handle_event', data)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.tableData[index].status = Number(res.status)
          this.tableData[index].reason = res.reason
        })
        .catch((response) => {
          this.$Message.error('提交失败')
        })
      },
      linkRejectPost (index) {
        if (this.tableData[index].status !== 1) {
          this.$Notice.error({
            title: '错误',
            desc: '您已经审核过该事件了'
          })
          return
        }
        let arr = this.tableData[index]
        var data = {
          id: arr.id,
          status: 3,
          reason: arr.reason
        }
        var name = this.tableData[index].contestant.user.contestant_user.name
        var id = this.tableData[index].contestant.user.id
        var content = '亲爱的＂' + name + '＂同学，你好，很遗憾你未能通过审核．'
        this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/personal_letter', {id: id, content: content})
        .then((response) => {
        })
        .catch((response) => {
        })
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/handle_event', data)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.tableData[index].status = Number(res.status)
          this.tableData[index].reason = res.reason
        })
        .catch((response) => {
          this.$Message.error('提交失败')
        })
      }
    }
  }
</script>

<style>
    .eventHandle-row{
        font-size: 15px;
        margin-top: 10px;
        margin-bottom:10px;
    }
    .eventHandle-modal{
        margin-left: 50px;
        margin-right: 50px;
        background: #fffacd;
        padding: 20px 40px 20px 40px;
    }
    .eventHandle-modal strong{
        font-size: 22px;
    }
</style>

