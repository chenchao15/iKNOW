<template>
  <div class="eventHandle">
    <Row class="eventHandle-row">
      <Col span="3" offset="13">
        <p style="margin-top:3px;font-weight: bold">组织者审核状态：</p>
      </Col>
      <Col span="5">
        <Select v-model="statusSelect" style="width:200px;margin-left:10px">
          <Option value=0 key="0">全部</Option>
          <Option value=1 key="1">未审核</Option>
          <Option value=2 key="2">已通过</Option>
          <Option value=3 key="3">未通过</Option>
        </Select>
      </Col>
      <Col span="3">
        <Button type="success" style="font-size:15px;margin-left:30px" @click="links(1)">点击筛选</Button>
      </Col>
    </Row>
    <Table :data="tableData" :columns="tableColumns1" stripe></Table>
    <Modal v-model="modifyModal" width="800">
      <p slot="header" style="color:#2d8cf0;text-align:center">
        <Icon type="information-circled"></Icon>
        <span>组织者审核</span>
      </p>
      <div class="eventHandle-modal">
        <div>
          <div v-for="i in currentEvent.items" :key="i.name">
            <Row>
              <Col span="5"><p style="font-size: 15px; font-weight:500;font-family: PingFang SC">{{i.name}}</p></Col>
              <Col span="19">
                <p v-if="i.type === 'Input'" style="font-size: 16px; font-family: KaiTi;word-break:break-all; word-wrap:break-word">{{i.value}}</p>
                <a v-if="i.type == 'Upload'" style="font-size: 16px; font-family: KaiTi;word-break:break-all; word-wrap:break-word">{{i.value}}</a>
              </Col>
            </Row>
          </div>
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
    data () {
      return {
        tableData: [],
        pageNum: 0,
        proPage: 1,
        eventNum: 10,
        modifyModal: false,
        currentEvent: {},
        signTable: [],
        statusSelect: '1',
        tableColumns1: [
          {
            title: '组织申请者',
            key: 'user',
            align: 'center',
            render: (h, params) => {
              const text = params.row.organizer.name
              return h('p', {
                style: {
                  fontSize: '14px'
                }
              }, text)
            }
          },
          {
            title: '更新时间',
            key: 'time',
            align: 'center',
            render: (h, params) => {
              return h('div', this.formatDate(this.tableData[params.index].time))
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
      this.statusSelect = '1'
    },
    mounted () {
      var dataGet = {
        status: Number(this.statusSelect)
      }
      this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/audit_number', {params: dataGet})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.pageNum = res.event_number
      })
      .catch((response) => {
        this.$Message.error('获取审核事件列表失败')
        this.pageNum = 0
      })
      this.signTable = [
        {name: '组织名称', type: 'Input', value: ''},
        {name: '简称', type: 'Input', value: ''},
        {name: '简介', type: 'Input', value: ''},
        {name: '领域', type: 'Input', value: ''},
        {name: '联系人', type: 'Input', value: ''},
        {name: '手机号', type: 'Input', value: ''},
        {name: '官方邮箱', type: 'Input', value: ''},
        {name: '地址', type: 'Input', value: ''},
        {name: '验证材料', type: 'Upload', value: ''}
      ]
      this.links(0)
    },
    methods: { // 当前阶段id: this.stageId
      links (page) { // {currentPage当前页，eventNum页面事件数，status事件状态(0:全部,1:未审核,2:已通过,3:未通过)}
        if (page === 1) {
          this.proPage = 1
        }
        var dataGet = {
          current_page: this.proPage,
          event_num: this.eventNum,
          status: Number(this.statusSelect)
        }
        this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/audit', {params: dataGet})
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          for (let i = 0; i < res.length; i++) {
            res[i].time = new Date()
            res[i].items = []
            res[i].items.push(res[i].content)
          }
          this.tableData = res
        })
        .catch((response) => {
          this.$Message.error('获取事件列表失败')
          this.tableData = []
        })
        console.log(dataGet)
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
        // The simulated data is changed directly here, and the actual usage scenario should fetch the data from the server
        this.proPage = count
        alert(this.proPage)
        this.links(0)
      },
      showDetail (index) {
        this.modifyModal = true
        let arr = this.tableData[index]
        this.currentEvent = {
          id: arr.id,
          items: '',
          next: index + 1,
          reason: arr.reason
        }
        this.currentEvent.items = this.signTable
        var len = this.currentEvent.items.length
        let i = 0
        for (i = 0; i < len; i++) {
          this.currentEvent.items[i].value = arr.items[i]
        }
      },
      linkPost (status) {
        var data = {
          id: this.currentEvent.id,
          status: status,
          reason: this.currentEvent.reason
        } // 这里将data抄送给后端，后端一定要返回status和reason,前端要将this.tableData[this.currentEvent.next - 1]的status和reason修改掉．从而显示修改后的状态
        this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/handle_audit', data)
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
          this.$Message.error('您已经审核到最后一个了')
        })
      },
      linkPassPost (index) {
        let arr = this.tableData[index]
        var data = {
          id: arr.id,
          status: 2,
          reason: arr.reason
        }
        this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/handle_audit', data)
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
        let arr = this.tableData[index]
        var data = {
          id: arr.id,
          status: 3,
          reason: arr.reason
        }
        this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/handle_audit', data)
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

