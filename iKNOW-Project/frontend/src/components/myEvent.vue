<template>
  <div class="eventHandle">
    <Table :data="tableData" :columns="tableColumns1" stripe></Table>
    <Modal v-model="detailModal" width="800">
      <div style="margin-top: 20px">
        <Row>
          <Col span="3">
            <p style="color:red; font-size: 17px">审批结果</p>
          </Col>
          <Col span="20">
            <p v-if="currentEvent.event_type !== 7" style="font-size: 16px; font-family: KaiTi;word-break:break-all; word-wrap:break-word">{{currentEvent.reason}}</p>
            <p v-else style="font-size: 16px; font-family: KaiTi;word-break:break-all; word-wrap:break-word">{{currentEvent.content}}</p>
          </Col>
        </Row>
      </div>
      <div slot="footer">
        <Button type="info" style="font-size: 16px" @click="sureClick">确定</Button>
      </div>
    </Modal>
    <Modal v-model="appealModal" width="800">
      <div>
        <strong>申诉理由</strong>
        <Input style="margin: 20px" type="textarea" v-model="appealReason" :autosize="{minRows: 3,maxRows: 5}"></Input>
      </div>
      <div slot="footer">
        <Button type="info" style="font-size: 16px" @click="linkAppealPost">确定</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
  export default {
    props: ['stageId'],
    data () {
      return {
        tableData: [],
        detailModal: false,
        appealModal: false,
        currentEvent: {},
        appealReason: '',
        tableColumns1: [
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
            width: 200,
            align: 'center',
            render: (h, params) => {
              if (params.row.type !== 7) {
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
                  }, '查看详情')
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
                        this.showDetail(params.index)
                      }
                    }
                  }, '查看详情'),
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
                        this.appeal(params.index)
                      }
                    }
                  }, '申诉')
                ])
              }
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
    mounted () { // 当前阶段id: this.stageId
      this.links()
    },
    methods: { // 当前阶段id: this.stageId
      links () {
        var dataGet = {
          phase_id: this.stageId
        }
        this.$http.get(this.GLOBAL.baseUrl + 'api/competition/event', {params: dataGet})
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          for (let i = 0; i < res.length; i++) {
            res[i].type = res[i].event_type
          }
          this.tableData = res
        })
        .catch((response) => {
          this.$Message.error('获取事件列表失败')
        })
      },
      showDetail (index) {
        this.currentEvent = this.tableData[index]
        this.detailModal = true
      },
      appeal (index) {
        this.appealModal = true
      },
      linkAppealPost () {
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/event', {phase_id: this.stageId, event_type: 3, content: this.appealReason, is_team: 0})
        .then((response) => {
          this.$Notice.success({
            title: '发起申诉审核中',
            desc: `发起申诉请求已发出，等待审核……`
          })
        })
        .catch((response) => {
          this.$Notice.error({
            title: '发起申诉请求失败',
            desc: `发起申诉请求失败……`
          })
        })
        this.appealModal = false
      },
      sureClick () {
        this.detailModal = false
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

