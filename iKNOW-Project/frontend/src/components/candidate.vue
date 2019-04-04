<template>
  <div v-if="existed == true">
    <Card>
      <Row class="button-choose" >
        <Col span="3" offset="4">
          <p class="sign-select">比赛阶段</p>
        </Col>
        <Col span="5">
          <Select v-model="selectStage">
            <Option v-for="item in stageItem" :value="item.name" :key="item.name">{{ item.name }}</Option>
            </Select>
        </Col>
        <Col v-if="selectStage !== ''" span="4" offset="1">
          <Button type="dashed" @click="addNewItem">选择对象</Button>
        </Col>
      </Row>
      <Modal v-model="itemModal" width="800" @on-ok="addPeople">
        <p slot="header" style="color:#2d8cf0; text-align:center;">
          <span>选择对象</span>
        </p>
        <div style="text-align:center; margin-bottom: 10px">
          <Row>
            <Select v-model="sortWay" style="width:100px;text-align:center;">
              <Option value="按值筛选">按值筛选</Option>
              <Option value="按名次筛选">按名次筛选</Option>
            </Select>
            <Select v-if="sortWay === '按值筛选'" v-model="selectPeople" style="width:70px;text-align:center;">
              <Option v-for="item in conditions" :value="item.value" :key="item.value"></Option>
            </Select>
            <Select v-model="filterDirection" style="width:70px;text-align:center;">
              <Option value="正选">正选</Option>
              <Option value="反选">反选</Option>
            </Select>
            <InputNumber :min="0" v-model="start_value" @on-change="startNumberChange"></InputNumber>
             ~ 
            <InputNumber :min="0" v-model="end_value" @on-change="endNumberChange"></InputNumber>
            <!--<Input v-model="searchValue" placeholder="关键字" style="width:120px;text-align:center;"></Input>-->
          </Row>
        </div>
        <div style="text-align:center; margin-bottom: 20px">
          <Button @click="startSearch">开始筛选</Button>
          <Button @click="continueSearch">继续筛选</Button>
        </div>
        <div>
          <Table border height="300" :columns="res_columns" :data="res_datas" @on-selection-change="selectChange"></Table>
        </div>
      </Modal>
      <div>
        <Table border height="300" :columns="chosen_columns" :data="chosen_datas"></Table>
      </div>
      <div style="margin-top: 5px;text-align:center;">
        <Button type="primary" v-on:click="confirmAllItem">确定已选对象</Button>
        <Col span="4"></Col>
        <Button type="ghost" @click="clearAllItem">清空已选对象</Button>
      </div>
    </Card>
  </div>
</template>

<script>
export default {
  name: 'candidate',
  props: ['comId'],
  data () {
    return {
      stageItem: [],
      selectStage: '',
      existed: true,
      selectPeople: '',
      filterDirection: '正选',
      sortWay: '按名次筛选',
      start_value: null,
      end_value: null,
      searchValue: null,
      itemModal: false,
      temp_datas: [],
      search_datas: [],
      res_datas: [],
      chosen_datas: [],
      filter_way: {
        filter_dir: '正选',
        sort_way: '按值筛选',
        min_value: 0,
        max_value: 0
      },
      conditions: [
        {
          value: '最新成绩',
          label: '最新成绩'
        },
        {
          value: '最高成绩',
          label: '最高成绩'
        }
      ],
      all_datas: [
      ],
      res_columns: [
        {
          type: 'selection',
          width: 60,
          align: 'center'
        },
        /* {
          title: '排名',
          key: 'ranking',
          width: 80,
          align: 'center',
          ellipsis: 'true',
          sortable: 'true'
        }, */
        {
          title: '姓名',
          key: 'name',
          align: 'center',
          ellipsis: 'true'
        },
        {
          title: '最新成绩',
          key: 'latest_grade',
          align: 'center',
          ellipsis: 'true',
          sortable: 'true'
        },
        {
          title: '最高成绩',
          key: 'highest_grade',
          align: 'center',
          ellipsis: 'true',
          sortable: 'true'
        }
      ],
      chosen_columns: [
        /* {
          title: '排名',
          key: 'ranking',
          width: 80,
          align: 'center',
          ellipsis: 'true',
          sortable: 'true'
        }, */
        {
          title: '姓名',
          key: 'name',
          align: 'center',
          ellipsis: 'true',
          render: (h, params) => {
            return h('div', [
              h('Icon', {
                props: {
                  type: 'person'
                }
              }),
              h('strong', params.row.name)
            ])
          }
        },
        {
          title: '最新成绩',
          key: 'latest_grade',
          align: 'center',
          ellipsis: 'true',
          sortable: 'true'
        },
        {
          title: '最高成绩',
          key: 'highest_grade',
          align: 'center',
          ellipsis: 'true',
          sortable: 'true'
        },
        {
          title: '操作',
          key: 'action',
          width: 150,
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
              }, '详情'),
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
      ]
    }
  },
  mounted () {
    this.links()
  },
  methods: {
    links () {  // 获取this.comId比赛的所有阶段
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/list_phase_simple?id=' + this.$route.params.id)
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.stageItem = [{name: '全部', id: -1}]
        for (var i in res) {
          this.stageItem.push(res[i])
        }
      })
      .catch((response) => {
        this.stageItem = [{name: '全部', id: -1}]
      })
    },
    addNewItem () {
      this.itemModal = true
      if (this.selectStage === '') {
        this.selectStage = this.stageItem[0].name
      }
      var selectId = -1
      for (var i in this.stageItem) {
        if (this.stageItem[i].name === this.selectStage) {
          selectId = this.stageItem[i].id
          break
        }
      }
      var dataGet = {
        phase_id: selectId,
        comp_id: this.$route.params.id
      }
      // 将this.comId和this.selectStage返回给后端获取人员列表
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/list_contestant', {params: dataGet})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.all_datas = []
        this.chosen_datas = []
        for (i in res) {
          var max = 0
          var latest = 0
          if (res[i].grade_max.submit_grade !== null) {
            max = res[i].grade_max.submit_grade
          }
          if (res[i].grade_latest.submit_grade === 0) {
            latest = res[i].grade_latest.submit_grade
          }
          this.all_datas.push({name: res[i].name, id: res[i].id, highest_grade: max, latest_grade: latest})
        }
        this.all_datas.sort(function (peoplea, peopleb) {
          return parseInt(peopleb.latest_grade) - parseInt(peoplea.latest_grade)
        })
        for (i = 0; i < this.all_datas.length; i++) {
          var index = parseInt(i) + 1
          this.all_datas[i]['ranking'] = index.toString()
        }
        this.res_datas = this.all_datas
      }).catch((response) => {
        this.all_datas = []
        this.$Message.error('获取人员数据表失败')
        this.res_datas = this.all_datas
          /* {
            name: 'John Brown',
            latest_grade: '87',
            highest_grade: '90'
          },
          {
            name: 'Jim Green',
            latest_grade: '80',
            highest_grade: '90'
          },
          {
            name: 'Joe Black',
            latest_grade: '75',
            highest_grade: '75'
          },
          {
            name: 'Jon Snow',
            latest_grade: '84',
            highest_grade: '94'
          }
        ]
        this.all_datas.sort(function (peoplea, peopleb) {
          return parseInt(peopleb.latest_grade) - parseInt(peoplea.latest_grade)
        })
        for (var i = 0; i < this.all_datas.length; i++) {
          var index = parseInt(i) + 1
          this.all_datas[i]['ranking'] = index.toString()
        } */
      })
    },
    confirmAllItem () {
      this.existed = false
      this.$Notice.success({
        title: '操作成功',
        desc: '您已选定对象！'
      })
      var anotherDatas = []
      for (var i in this.chosen_datas) {
        anotherDatas.push(this.chosen_datas[i].id)
      }
      console.log(anotherDatas)
      this.$emit('message', anotherDatas)
    },
    clearAllItem () {
      this.chosen_datas = []
    },
    show (index) {
      this.$Modal.info({
        title: '参赛者信息',
        content: `名字：${this.chosen_datas[index].name}<br>排名：${this.chosen_datas[index].ranking}<br>成绩：${this.chosen_datas[index].grade}`
      })
    },
    remove (index) {
      this.chosen_datas.splice(index, 1)
    },
    startSearch () {
      this.search_datas = []
      var flag = this.parseFilter()
      if (!flag && this.selectPeople === '') {
        this.search_datas = this.all_datas
      } else if (this.sortWay === '按名次筛选') {
        if (this.filterDirection === '正选') {
          for (var i in this.all_datas) {
            if (parseInt(this.all_datas[i].ranking) <= parseInt(this.filter_way.max_value) && parseInt(this.all_datas[i].ranking) >= parseInt(this.filter_way.min_value)) {
              this.search_datas.push(this.all_datas[i])
            }
          }
          this.search_datas.sort(function (peoplea, peopleb) {
            return peoplea.ranking - peopleb.ranking
          })
        } else if (this.filterDirection === '反选') {
          for (i in this.all_datas) {
            if (this.all_datas[i].ranking <= this.filter_way.max_value || this.all_datas[i].ranking >= this.filter_way.min_value) {
              this.search_datas.push(this.all_datas[i])
            }
          }
          this.search_datas.sort(function (peoplea, peopleb) {
            return parseInt(peoplea.ranking) - parseInt(peopleb.ranking)
          })
        }
      } else if (this.sortWay === '按值筛选') {
        if (this.filterDirection === '正选') {
          if (this.selectPeople === '最新成绩') {
            for (i in this.all_datas) {
              if (parseInt(this.all_datas[i].latest_grade) <= parseInt(this.filter_way.max_value) && parseInt(this.all_datas[i].latest_grade) >= parseInt(this.filter_way.min_value)) {
                this.search_datas.push(this.all_datas[i])
              }
            }
            this.search_datas.sort(function (peoplea, peopleb) {
              return parseInt(peopleb.latest_grade) - parseInt(peoplea.latest_grade)
            })
          } else if (this.selectPeople === '最高成绩') {
            for (i in this.all_datas) {
              if (parseInt(this.all_datas[i].highest_grade) <= parseInt(this.filter_way.max_value) && parseInt(this.all_datas[i].highest_grade) >= parseInt(this.filter_way.min_value)) {
                this.search_datas.push(this.all_datas[i])
              }
            }
            this.search_datas.sort(function (peoplea, peopleb) {
              return parseInt(peopleb.highest_grade) - parseInt(peoplea.highest_grade)
            })
          }
        } else if (this.filterDirection === '反选') {
          if (this.selectPeople === '最新成绩') {
            for (i in this.all_datas) {
              if (parseInt(this.all_datas[i].latest_grade) <= parseInt(this.filter_way.max_value) || parseInt(this.all_datas[i].latest_grade) >= parseInt(this.filter_way.min_value)) {
                this.search_datas.push(this.all_datas[i])
              }
            }
            this.search_datas.sort(function (peoplea, peopleb) {
              return parseInt(peopleb.latest_grade) - parseInt(peoplea.latest_grade)
            })
          } else if (this.selectPeople === '最高成绩') {
            for (i in this.all_datas) {
              if (parseInt(this.all_datas[i].highest_grade) <= parseInt(this.filter_way.max_value) || parseInt(this.all_datas[i].highest_grade) >= parseInt(this.filter_way.min_value)) {
                this.search_datas.push(this.all_datas[i])
              }
            }
            this.search_datas.sort(function (peoplea, peopleb) {
              return parseInt(peopleb.highest_grade) - parseInt(peoplea.highest_grade)
            })
          }
        }
      }
      this.res_datas = this.search_datas
      this.restoreData()
    },
    continueSearch () {
      var prevSearchDatas = this.search_datas
      this.search_datas = []
      var flag = this.parseFilter()
      if (!flag && this.selectPeople === '') {
        this.search_datas = prevSearchDatas
      } else if (this.sortWay === '按名次筛选') {
        if (this.filterDirection === '正选') {
          for (var i in prevSearchDatas) {
            if (prevSearchDatas[i].ranking <= this.filter_way.max_value && prevSearchDatas[i].ranking >= this.filter_way.min_value) {
              this.search_datas.push(prevSearchDatas[i])
            }
          }
          this.search_datas.sort(function (peoplea, peopleb) {
            return peoplea.ranking - peopleb.ranking
          })
        } else if (this.filterDirection === '反选') {
          for (i in prevSearchDatas) {
            if (prevSearchDatas[i].ranking <= this.filter_way.max_value || prevSearchDatas[i].ranking >= this.filter_way.min_value) {
              this.search_datas.push(prevSearchDatas[i])
            }
          }
          this.search_datas.sort(function (peoplea, peopleb) {
            return peoplea.ranking - peopleb.ranking
          })
        }
      } else if (this.sortWay === '按值筛选') {
        if (this.filterDirection === '正选') {
          if (this.selectPeople === '最新成绩') {
            for (i in prevSearchDatas) {
              if (prevSearchDatas[i].latest_grade <= this.filter_way.max_value && prevSearchDatas[i].latest_grade >= this.filter_way.min_value) {
                this.search_datas.push(prevSearchDatas[i])
              }
            }
            this.search_datas.sort(function (peoplea, peopleb) {
              return peopleb.latest_grade - peoplea.latest_grade
            })
          } else if (this.selectPeople === '最高成绩') {
            for (i in prevSearchDatas) {
              if (prevSearchDatas[i].highest_grade <= this.filter_way.max_value && prevSearchDatas[i].highest_grade >= this.filter_way.min_value) {
                this.search_datas.push(prevSearchDatas[i])
              }
            }
            this.search_datas.sort(function (peoplea, peopleb) {
              return peopleb.highest_grade - peoplea.highest_grade
            })
          }
        } else if (this.filterDirection === '反选') {
          if (this.selectPeople === '最新成绩') {
            for (i in prevSearchDatas) {
              if (prevSearchDatas[i].latest_grade <= this.filter_way.max_value || prevSearchDatas[i].latest_grade >= this.filter_way.min_value) {
                this.search_datas.push(prevSearchDatas[i])
              }
            }
            this.search_datas.sort(function (peoplea, peopleb) {
              return peopleb.latest_grade - peoplea.latest_grade
            })
          } else if (this.selectPeople === '最高成绩') {
            for (i in prevSearchDatas) {
              if (prevSearchDatas[i].highest_grade <= this.filter_way.max_value || prevSearchDatas[i].highest_grade >= this.filter_way.min_value) {
                this.search_datas.push(prevSearchDatas[i])
              }
            }
            this.search_datas.sort(function (peoplea, peopleb) {
              return peopleb.highest_grade - peoplea.highest_grade
            })
          }
        }
      }
      this.res_datas = this.search_datas
      this.restoreData()
    },
    addPeople () {
      if (this.chosen_datas === null) {
        this.chosen_datas = this.temp_datas
      } else {
        for (var i in this.temp_datas) {
          var flag = false
          for (var j in this.chosen_datas) {
            if (this.temp_datas[i].name === this.chosen_datas[j].name) {
              flag = true
            }
          }
          if (!flag) {
            this.chosen_datas.push(this.temp_datas[i])
          }
        }
      }
      this.res_datas = this.all_datas
    },
    selectChange (selection) {
      this.temp_datas = selection
    },
    startNumberChange (value) {
      this.start_value = value
    },
    endNumberChange (value) {
      this.end_value = value
    },
    restoreData () {
      this.selectPeople = ''
      // this.filterDirection = '正选'
      // this.sortWay = '按名次筛选'
      this.start_value = null
      this.end_value = null
      this.searchValue = null
    },
    parseFilter () {
      var flag = true
      this.filter_way.filter_dir = this.filterDirection
      this.filter_way.sort_way = this.sortWay
      if (this.start_value === null && this.end_value !== null) {
        if (this.filterDirection === '正选') {
          this.filter_way.min_value = 0
          this.filter_way.max_value = this.end_value
        } else if (this.filterDirection === '反选') {
          this.filter_way.min_value = this.end_value + 1
          this.filter_way.max_value = -1
        }
      } else if (this.start_value !== null && this.end_value === null) {
        if (this.filterDirection === '正选') {
          this.filter_way.min_value = this.start_value
          this.filter_way.max_value = 0
        } else if (this.filterDirection === '反选') {
          this.filter_way.min_value = 100000
          this.filter_way.max_value = this.start_value - 1
        }
      } else if (this.start_value !== null && this.end_value !== null) {
        if (this.start_value > this.end_value) {
          this.start_value = null
          this.end_value = null
          flag = false
          this.$Notice.error({
            title: '错误',
            desc: '所选范围无效，请重新填选'
          })
        } else {
          if (this.filterDirection === '正选') {
            this.filter_way.min_value = this.start_value
            this.filter_way.max_value = this.end_value
          } else if (this.filterDirection === '反选') {
            this.filter_way.min_value = this.end_value + 1
            this.filter_way.max_value = this.start_value - 1
          }
        }
      } else {
        flag = false
      }
      return flag
    }
  }
}
</script>
<style>
  .button-choose{
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
  }
  .button-reset{
    margin-top: 20px;
    padding: 5px;
    font-size: 10px;
    font-color: #aaa;
    font-weight: bold;
    text-align: center;
  }
  .select{
    width: 70px;
    text-align: center;
  }
  .sign-select{
    font-size: 14px;
    margin-top: 4px;
  }
</style>
