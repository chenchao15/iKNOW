<template>
  <div>
    <Row style="margin-bottom: 20px">
      <Col span="18">
        <h1>阶段信息</h1>
      </Col>
      <Col span="6">
        <Button style="font-size:17px;font-weight:bold" type="dashed" @click="createNewStageInit"><Icon type="plus-round"></Icon> 创建新的比赛阶段</Button>
      </Col>
    </Row>
    <Table border :columns="stageColumns" :data="stageData"></Table>
    <Modal v-model="deleteModal" width="360">
      <p slot="header" style="color:#f60;text-align:center">
        <Icon type="information-circled"></Icon>
        <span>删除</span>
      </p>
      <div style="text-align:center">
        <p>删除该阶段将导致有关该阶段的所有信息都将删除，包括参赛人员信息等</p>
        <p style="font-weight: bold">您确定要删除吗？</p>
      </div>
      <div slot="footer">
        <Button type="error" size="large" long :loading="modalLoading" @click="del">继续删除</Button>
      </div>
    </Modal>
    <Modal v-model="stageModal" width="900">
      <p slot="header" style="color:#2d8cf0;text-align:center;font-size:20px">
        <Icon type="flag"></Icon>
        <span>创建一个新的比赛阶段</span>
      </p>
      <div style="text-align:center;margin-bottom:20px">
        <p>你可以创建例如"初赛","复赛","决赛","加赛"或者更多比赛阶段</p>
        <p style="color:red">请注意后创建的比赛阶段时间不能先于之前的比赛阶段</p>
      </div>
      <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100">
        <FormItem label="比赛阶段名称" prop="name">
          <Input v-model="formValidate.name" placeholder="请选择比赛阶段"></Input>
        </FormItem>
        <Row>
          <Col span="10">
            <FormItem label="参赛形式" prop="issingle">
              <RadioGroup v-model="formValidate.issingle">
                <Radio label="个人赛">个人赛</Radio>
                <Radio label="小组赛">小组赛</Radio>
              </RadioGroup>
            </FormItem>
          </Col>
          <div v-if="formValidate.issingle === '小组赛'">
          <Col span="5">
            <FormItem label="参赛人数" prop="minp">
              <InputNumber :max="20" :min="1" v-model="formValidate.minp"></InputNumber>
            </FormItem>
          </Col>
          <Col span="1">
            <p style="text-align:center; margin-top:8px">~</p>
          </Col>
          <Col span="2">
            <InputNumber :max="20" :min="1" v-model="formValidate.maxp"></InputNumber>
          </Col>
          <Col span="1">
            <p style="text-align:center; margin-top:8px">人</p>
          </Col>
          </div>
        </Row>
        <FormItem label="参赛途径" prop="way" v-if="this.stageData.length !== 0">
          <CheckboxGroup v-model="formValidate.way">
            <Checkbox label="允许报名"></Checkbox>
          </CheckboxGroup>
        </FormItem>
        <Row v-if="formValidate.way[0]==='允许报名'|| this.stageData.length === 0">
          <Col span='12'>
            <FormItem label="报名开始时间">
              <Row>
                <Col span="11">
                  <FormItem prop="signstartdate">
                    <DatePicker type="date" placeholder="报名开始日期" v-model="formValidate.signstartdate"></DatePicker>
                  </FormItem>
                </Col>
                <Col span="1" style="text-align: center">-</Col>
                <Col span="11">
                  <FormItem prop="signstarttime">
                    <TimePicker type="time" placeholder="报名开始时间" v-model="formValidate.signstarttime"></TimePicker>
                  </FormItem>
                </Col>
              </Row>
            </FormItem>
          </Col>
          <Col span='12'>
            <FormItem label="报名结束时间">
              <Row>
                <Col span="11">
                  <FormItem prop="signenddate">
                    <DatePicker type="date" placeholder="报名结束日期" v-model="formValidate.signenddate"></DatePicker>
                  </FormItem>
                </Col>
                <Col span="1" style="text-align: center">-</Col>
                <Col span="11">
                  <FormItem prop="signendtime">
                    <TimePicker type="time" placeholder="报名结束时间" v-model="formValidate.signendtime"></TimePicker>
                  </FormItem>
                </Col>
              </Row>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span='12'>
            <FormItem label="比赛开始时间">
              <Row>
                <Col span="11">
                  <FormItem prop="startdate">
                    <DatePicker type="date" placeholder="比赛开始日期" v-model="formValidate.startdate"></DatePicker>
                  </FormItem>
                </Col>
                <Col span="1" style="text-align: center">-</Col>
                <Col span="11">
                  <FormItem prop="starttime">
                    <TimePicker type="time" placeholder="比赛开始时间" v-model="formValidate.starttime"></TimePicker>
                  </FormItem>
                </Col>
              </Row>
            </FormItem>
          </Col>
          <Col span='12'>
            <FormItem label="比赛结束时间">
              <Row>
                <Col span="11">
                  <FormItem prop="enddate">
                    <DatePicker type="date" placeholder="比赛结束日期" v-model="formValidate.enddate"></DatePicker>
                  </FormItem>
                </Col>
                <Col span="1" style="text-align: center">-</Col>
                <Col span="11">
                  <FormItem prop="endtime">
                    <TimePicker type="time" placeholder="比赛结束时间" v-model="formValidate.endtime"></TimePicker>
                  </FormItem>
                </Col>
              </Row>
            </FormItem>
          </Col>
        </Row>
      </Form>
      <div slot="footer">
        <Row>
          <Col span="14" offset="5">
            <Button type="info" size="large" long :loading="modalLoading" @click="createNewStage('formValidate')">创建</Button>
          </Col>
        </Row>
      </div>
    </Modal>
    <Modal v-model="modifyModal" width="900">
      <p slot="header" style="color:#2d8cf0;text-align:center;font-size:20px">
        <Icon type="flag"></Icon>
        <span>修改当前比赛阶段</span>
      </p>
      <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100">
        <FormItem label="比赛阶段名称" prop="name">
          <Input v-model="formValidate.name" placeholder="请选择比赛阶段"></Input>
        </FormItem>
        <Row>
          <Col span="10">
            <FormItem label="参赛形式" prop="issingle">
              <RadioGroup v-model="formValidate.issingle">
                <Radio label="个人赛">个人赛</Radio>
                <Radio label="小组赛">小组赛</Radio>
              </RadioGroup>
            </FormItem>
          </Col>
          <div v-if="formValidate.issingle === '小组赛'">
          <Col span="5">
            <FormItem label="参赛人数" prop="minp">
              <InputNumber :max="20" :min="1" v-model="formValidate.minp"></InputNumber>
            </FormItem>
          </Col>
          <Col span="1">
            <p style="text-align:center; margin-top:8px">~</p>
          </Col>
          <Col span="2">
            <InputNumber :max="20" :min="1" v-model="formValidate.maxp"></InputNumber>
          </Col>
          <Col span="1">
            <p style="text-align:center; margin-top:8px">人</p>
          </Col>
          </div>
        </Row>
        <FormItem label="参赛途径" prop="way">
          <CheckboxGroup v-model="formValidate.way">
            <Checkbox label="允许报名"></Checkbox>
          </CheckboxGroup>
        </FormItem>
        <Row v-if="formValidate.way[0]==='允许报名'|| this.stageData.length === 0">
          <Col span='12'>
            <FormItem label="报名开始时间">
              <Row>
                <Col span="11">
                  <FormItem prop="signstartdate">
                    <DatePicker type="date" placeholder="报名开始日期" v-model="formValidate.signstartdate"></DatePicker>
                  </FormItem>
                </Col>
                <Col span="1" style="text-align: center">-</Col>
                <Col span="11">
                  <FormItem prop="signstarttime">
                    <TimePicker type="time" placeholder="报名开始时间" v-model="formValidate.signstarttime"></TimePicker>
                  </FormItem>
                </Col>
              </Row>
            </FormItem>
          </Col>
          <Col span='12'>
            <FormItem label="报名结束时间">
              <Row>
                <Col span="11">
                  <FormItem prop="signenddate">
                    <DatePicker type="date" placeholder="报名结束日期" v-model="formValidate.signenddate"></DatePicker>
                  </FormItem>
                </Col>
                <Col span="1" style="text-align: center">-</Col>
                <Col span="11">
                  <FormItem prop="signendtime">
                    <TimePicker type="time" placeholder="报名结束时间" v-model="formValidate.signendtime"></TimePicker>
                  </FormItem>
                </Col>
              </Row>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span='12'>
            <FormItem label="比赛开始时间">
              <Row>
                <Col span="11">
                  <FormItem prop="startdate">
                    <DatePicker type="date" placeholder="比赛开始日期" v-model="formValidate.startdate"></DatePicker>
                  </FormItem>
                </Col>
                <Col span="1" style="text-align: center">-</Col>
                <Col span="11">
                  <FormItem prop="starttime">
                    <TimePicker type="time" placeholder="比赛开始时间" v-model="formValidate.starttime"></TimePicker>
                  </FormItem>
                </Col>
              </Row>
            </FormItem>
          </Col>
          <Col span='12'>
            <FormItem label="比赛结束时间">
              <Row>
                <Col span="11">
                  <FormItem prop="enddate">
                    <DatePicker type="date" placeholder="比赛结束日期" v-model="formValidate.enddate"></DatePicker>
                  </FormItem>
                </Col>
               <Col span="1" style="text-align: center">-</Col>
                <Col span="11">
                  <FormItem prop="endtime">
                    <TimePicker type="time" placeholder="比赛结束时间" v-model="formValidate.endtime"></TimePicker>
                  </FormItem>
                </Col>
              </Row>
            </FormItem>
          </Col>
        </Row>
      </Form>
      <div slot="footer">
        <Row>
          <Col span="14" offset="5">
            <Button type="info" size="large" long :loading="modalLoading" @click="modifyStage('formValidate')">确定</Button>
          </Col>
        </Row>
      </div>
    </Modal>
    <Modal v-model="detailModal" width="500">
      <p slot="header" style="color:#2d8cf0;text-align:center">
        <Icon type="information-circled"></Icon>
        <span>阶段信息</span>
      </p>
      <div class="stage-detailModal">
        <p><span>阶段名称：</span>{{this.stageDetail.name}}</p>
        <p v-if="this.stageDetail.max_group == 1 "><span>阶段形式：</span>个人赛</p>
        <p v-else><span>阶段形式：</span>小组赛（{{this.stageDetail.min_group}} ~ {{this.stageDetail.max_group}}人）</p>
        <p v-if="this.stageDetail.able_to_sign == 1"><span>是否允许报名：</span>是</p>
        <p v-else><span>是否允许报名：</span>否</p>
        <p v-if="this.stageDetail.able_to_sign == 1"><span>报名时间：</span>{{this.stageDetail.sign_start_time}} ~ {{this.stageDetail.sign_end_time}}</p>
        <p><span>比赛时间：</span>{{this.stageDetail.start_time}} ~ {{this.stageDetail.end_time}}</p>
      </div>
      <div slot="footer">
        <Button type="primary" size="large" long @click="closeShow">确定</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
export default {
  name: 'stageManage',
  data () {
    return {
      deleteModal: false,
      modifyModal: false,
      stageModal: false,
      detailModal: false,
      modalLoading: false,
      index: 0,
      formValidate: {
        name: '',
        way: [],
        issingle: '',
        minp: 1,
        maxp: 1,
        signstartdate: '',
        signenddate: '',
        signstarttime: '',
        signendtime: '',
        startdate: '',
        enddate: '',
        starttime: '',
        endtime: ''
      },
      stageDetail: {},
      ruleValidate: {
        name: [
          { required: true, message: '请选择比赛阶段', trigger: 'change' }
        ],
        issingle: [
          { required: true, message: '请选择比赛形式', trigger: 'change' }
        ],
        signstartdate: [
          { required: true, type: 'date', message: '请选择报名开始日期', trigger: 'change' }
        ],
        signenddate: [
          { required: true, type: 'date', message: '请选择报名结束日期', trigger: 'change' }
        ],
        startdate: [
          { required: true, type: 'date', message: '请选择比赛开始日期', trigger: 'change' }
        ],
        enddate: [
          { required: true, type: 'date', message: '请选择比赛结束日期', trigger: 'change' }
        ],
        signstarttime: [
          { required: true, type: 'date', message: '请选择报名开始时间', trigger: 'change' }
        ],
        signendtime: [
          { required: true, type: 'date', message: '请选择报名结束时间', trigger: 'change' }
        ],
        starttime: [
          { required: true, type: 'date', message: '请选择比赛开始时间', trigger: 'change' }
        ],
        endtime: [
          { required: true, type: 'date', message: '请选择报名结束时间', trigger: 'change' }
        ]
      },
      stageColumns: [
        {
          title: '阶段名称',
          key: 'name',
          width: 130,
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Icon', {
                props: {
                  type: 'flag'
                }
              }),
              h('strong', {
              }, params.row.name)
            ])
          }
        },
        {
          title: '允许报名',
          key: 'able_to_sign',
          width: 85,
          align: 'center',
          render: (h, params) => {
            if (params.row.able_to_sign === 0) {
              return h('div', [
                h('strong', {
                  style: {
                    color: 'red'
                  }
                }, '否')
              ])
            } else if (params.row.able_to_sign === 1) {
              return h('div', [
                h('strong', {
                  style: {
                    color: 'red'
                  }
                }, '是')
              ])
            }
          }
        },
        {
          title: '比赛开始时间',
          key: 'start_time',
          align: 'center'
        },
        {
          title: '比赛结束时间',
          key: 'end_time',
          align: 'center'
        },
        {
          title: '选项',
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
                    this.show(params.index)
                  }
                }
              }, '查看详情'),
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
                    this.modify(params.index)
                  }
                }
              }, '修改'),
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.remove(params.index)
                  }
                }
              }, '删除')
            ])
          }
        }
      ],
      stageData: [
      ]
    }
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/competitionmanage/' + this.$route.params.id) {
        this.links()
      }
    }
  },
  mounted () {
    this.links()
  },
  methods: {
    links () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/listPhase?id=' + this.$route.params.id)
          .then((response) => {
            var res0 = JSON.parse(response.bodyText)
            /*  end_time: "2017-12-06 21:55:00"
                able_to_sign: 0
                enrolment_method: "1"
                id: 1
                max_group: 1
                min_group: 1
                name: "000"
                sign_end_time: "2017-12-06 21:55:00"
                sign_start_time: "2017-12-06 21:55:00"
                start_time: "2017-12-06 21:55:00"
                status: 0  */
            this.stageData = res0
            // to do
          }).catch((response) => {
            this.stageData = []
          })
    },
    show (index) {
      this.stageDetail = this.stageData[index]
      this.detailModal = true
    },
    closeShow () {
      this.detailModal = false
    },
    modify (index) {
      this.modifyModal = true
      this.index = index
      this.formValidate.name = this.stageData[index].name
      this.formValidate.issingle = ''
      this.formValidate.minp = 1
      this.formValidate.maxp = 1
      this.formValidate.way.length = 0
      this.formValidate.signstartdate = ''
      this.formValidate.signenddate = ''
      this.formValidate.signstarttime = ''
      this.formValidate.signendtime = ''
      this.formValidate.startdate = ''
      this.formValidate.enddate = ''
      this.formValidate.starttime = ''
      this.formValidate.endtime = ''
    },
    remove (index) {
      this.deleteModal = true
      this.index = index
    },
    createNewStageInit () {
      this.stageModal = true
      this.formValidate.name = ''
      this.formValidate.issingle = ''
      this.formValidate.minp = 1
      this.formValidate.maxp = 1
      this.formValidate.way.length = 0
      this.formValidate.signstartdate = ''
      this.formValidate.signenddate = ''
      this.formValidate.signstarttime = ''
      this.formValidate.signendtime = ''
      this.formValidate.startdate = ''
      this.formValidate.enddate = ''
      this.formValidate.starttime = ''
      this.formValidate.endtime = ''
      this.$refs['formValidate'].resetFields()
    },
    del () {
      this.modalLoading = true
      setTimeout(() => {
        this.modalLoading = false
        this.deleteModal = false
        var stageid = this.stageData[this.index].id
        // this.stageData.splice(this.index, 1)
        this.linkDeletePost(stageid)
        this.links()
        this.$Message.success('删除成功')
      }, 1500)
    },
    createNewStage (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          if (this.inputCheck(this.formValidate)) {
            this.modalLoading = true
            setTimeout(() => {
              this.modalLoading = false
              this.stageModal = false
              this.linkSinglePost()
              this.$Message.success('创建成功')
            }, 2000)
          }
        } else {
          this.$Message.error('您还有未填写的信息')
        }
      })
    },
    modifyStage (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          if (this.inputCheck(this.formValidate)) {
            this.modalLoading = true
            setTimeout(() => {
              this.modalLoading = false
              this.modifyModal = false
              this.linkModifyPost(this.stageData[this.index].id)
              this.$Message.success('修改成功')
            }, 2000)
          }
        } else {
          this.$Message.error('您还有未填写的信息')
        }
      })
    },
    getSignDateTime (dates, times) {
      if (this.formValidate.way[0] === '允许报名' || this.stageData.length === 0) {
        dates = new Date(Date.parse(dates))
        times = new Date(Date.parse(times))
        times.setFullYear(dates.getFullYear())
        times.setMonth(dates.getMonth())
        times.setDate(dates.getDate())
        return Number(times)
      } else {
        return 0
      }
    },
    getDateTime (dates, times) {
      dates = new Date(Date.parse(dates))
      times = new Date(Date.parse(times))
      times.setFullYear(dates.getFullYear())
      times.setMonth(dates.getMonth())
      times.setDate(dates.getDate())
      return Number(times)
    },
    inputCheck (form) {
      var szMsg = '[{}#_%&/",;:=!^?*~，．？：＂！＃＆；＾｛｝]'
      var alertstr1 = ''
      var i
      for (i = 0; i < form.name.length; i++) {
        if (form.name.indexOf(szMsg[i]) > -1) {
          alertstr1 = '请不要在比赛名称中包含有非法字符[]{}#_%&/",;:=!^?*等'
          break
        }
      }
      var alertstr2 = ''
      if (form.startdate > form.enddate) {
        alertstr2 = '比赛阶段开始时间不能晚于比赛结束时间'
      } else if (form.startdate < form.enddate) {
        alertstr2 = ''
      } else if (form.starttime >= form.endtime) {
        alertstr2 = '比赛阶段开始时间不能晚于比赛结束时间'
      }
      var alertstr3 = ''
      var alertstr4 = ''
      if (form.way[0] === '允许报名' || this.stageData.length === 0) {
        if (form.signstartdate > form.startdate) {
          alertstr3 = '比赛阶段开始时间不能早于报名开始时间'
        } else if (form.signstartdate < form.startdate) {
          alertstr3 = ''
        } else if (form.signstarttime >= form.starttime) {
          alertstr3 = '比赛阶段开始时间不能早于报名开始时间'
        }
        if (form.signstartdate > form.signenddate) {
          alertstr4 = '报名开始时间不能晚于报名结束时间'
        } else if (form.signstartdate < form.signenddate) {
          alertstr4 = ''
        } else if (form.signstarttime >= form.signendtime) {
          alertstr4 = '报名开始时间不能晚于报名结束时间'
        }
      }
      if (alertstr1 !== '') {
        this.$Notice.error({
          title: '阶段名称错误',
          desc: alertstr1
        })
        return false
      } else if (alertstr2 !== '') {
        this.$Notice.error({
          title: '时间错误',
          desc: alertstr2
        })
        return false
      } else if (alertstr3 !== '') {
        this.$Notice.error({
          title: '时间错误',
          desc: alertstr3
        })
        return false
      } else if (alertstr4 !== '') {
        this.$Notice.error({
          title: '时间错误',
          desc: alertstr4
        })
        return false
      } else {
        return true
      }
    },
    linkSinglePost () {
      var dataTest = {
        id: this.$route.params.id,
        name: this.formValidate.name,
        able_to_sign: (this.formValidate.way[0] === '允许报名' || this.stageData.length === 0) ? 1 : 0,
        max_group: this.formValidate.maxp,
        min_group: this.formValidate.minp,
        signstarttime: this.getSignDateTime(this.formValidate.signstartdate, this.formValidate.signstarttime),
        signendtime: this.getSignDateTime(this.formValidate.signenddate, this.formValidate.signendtime),
        starttime: this.getDateTime(this.formValidate.startdate, this.formValidate.starttime),
        endtime: this.getDateTime(this.formValidate.enddate, this.formValidate.endtime)
      }
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/createPhase', dataTest)
          .then((response) => {
            this.links()
          }).catch((response) => {
          })
    },
    linkModifyPost (id) {
      var dataTest = {
        id: id,
        name: this.formValidate.name,
        able_to_sign: (this.formValidate.way[0] === '允许报名' || this.stageData.length === 0) ? 1 : 0,
        max_group: this.formValidate.maxp,
        min_group: this.formValidate.minp,
        signstarttime: this.getSignDateTime(this.formValidate.signstartdate, this.formValidate.signstarttime),
        signendtime: this.getSignDateTime(this.formValidate.signenddate, this.formValidate.signendtime),
        starttime: this.getDateTime(this.formValidate.startdate, this.formValidate.starttime),
        endtime: this.getDateTime(this.formValidate.enddate, this.formValidate.endtime)
      }
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/detailPhase/' + id, dataTest)
          .then((response) => {
            this.links()
          }).catch((response) => {
          })
    },
    linkDeletePost (id) {
      this.$http.delete(this.GLOBAL.baseUrl + 'api/competition/detailPhase/' + id)
          .then((response) => {
            this.links()
          }).catch((response) => {
          })
    }
  }
}
</script>

<style>
    .stage-btn{
        font-size: 17px;
        font-weight: bold;
    }
    .stage-detailModal{
        margin-left: 30px;
    }
    .stage-detailModal p{
        font-family: FangSong;
        font-size: 17px;
    }
    .stage-detailModal span{
        font-weight: bold;
    }
</style>
