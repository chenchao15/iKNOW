<template>
<div>
  <navigationBar></navigationBar>
  <div class="searchlayout">
    <div class="searchlayout-content">
      <div class="searchlayout-content-main">
        <p class="searchlayout-content-p">共搜索到{{this.searchData.length}}条结果</p>
        <div v-if="this.$route.params.type === '0'">
          <div v-for="(i, index) in eachPageData" :key="i.id">
            <Col span="7" v-if="index % 3 === 0" style="margin-bottom: 15px">
              <Card style="width:320px; background:#dddee1">
                <div style="text-align:center">
                  <a @click="clickCmpDetail(i.id)"><img width="270px" height="150px" :src="i.pic_url"/></a>
                  <h4>{{i.name}}</h4>
                </div>
              </Card>
            </Col>
            <Col span="7" offset="1" v-if="index % 3 !== 0" style="margin-bottom: 15px">
              <Card style="width:320px; background:#dddee1">
                <div style="text-align:center">
                  <a @click="clickCmpDetail(i.id)"><img width="270px" height="150px" :src="i.pic_url"/></a>
                  <h4>{{i.name}}</h4>
                </div>
              </Card>
            </Col>
          </div>
        </div>
        <div v-if="this.$route.params.type === '1'">
          <div v-for="(i, index) in eachPageData" :key="i.id">
            <Card style="width:600px;margin-bottom: 10px">
              <Row>
                <Col span="19">
                  <a @click="clickGroDetail(i.user)"><h3 style="word-break:break-all; word-wrap:break-word">{{i.user.organizer_user.name}}</h3></a>
                  <p class="searchlayout-group-p"><strong>领域: </strong>{{i.field}}</p>
                  <p class="searchlayout-group-p"><strong>联系人: </strong>{{i.contact}}</p>
                  <p class="searchlayout-group-p"><strong>联系电话: </strong>{{i.contact_number}}</p>
                  <p class="searchlayout-group-p"><strong>官方邮箱: </strong>{{i.contact_email}}</p>
                </Col>
                <Col span="5">
                  <a @click="clickGroDetail(i.user)"><img class="searchlayout-group-img" :src="i.avatar_url"/></a>
                </Col>
              </Row>
            </Card>
          </div>
        </div>
        <div v-if="this.$route.params.type === '2'">
          <div v-for="(i, index) in eachPageData" :key="i.id">
            <Card style="width:600px;margin-bottom: 10px">
              <a @click="clickTotDetail(i.id)"><h3 style="word-break:break-all; word-wrap:break-word">{{i.title}}</h3></a>
              <p class="searchlayout-group-p" v-if="i.author.contestant_user === null"><strong>作者: </strong>{{i.author.organizer_user.name}}</p>
              <p class="searchlayout-group-p" v-else><strong>作者: </strong>{{i.author.contestant_user.name}}</p>
              <p class="searchlayout-group-p"><strong>发布时间: </strong>{{i.post_time}}</p>
            </Card>
          </div>
        </div>
        <div v-if="this.$route.params.type === '3'">
          <div v-for="(i, index) in eachPageData" :key="i.id">
            <Card style="width:600px;margin-bottom: 10px">
              <Row>
                <Col span="25">
                  <Row>
                    <Col span="2">
                      <Tag type="border">{{i.isLike}}</Tag>
                    </Col>
                    <Col span="15">
                      <a @click="clickTalkDetail(i.id)">{{i.title}}</a>
                    </Col>
                    <Col span="3">
                      <p><Icon type="ios-person"></Icon>{{stringCut(i.author.name)}}</p>
                    </Col>
                    <Col span="3" offset="1">
                      <p style="font-size:13px;color:#9ea7b4">{{i.createTime}}</p>
                    </Col>
                  </Row>
                </Col>
              </Row>
            </Card>
          </div>
        </div>
        <div v-if="this.$route.params.type === 'none'">
        </div>
      </div>
    </div>
    <div class="searchlayout-page">
      <Page :total="pageNum" :current="currentPage" @on-change="changePage" show-elevator></Page>    
    </div>
    <div class="searchlayout-copy">
        2011-2017 &copy; iKNOW
    </div>
  </div>
</div>
</template>

<script>
import navigationBar from '../components/navigationBar'
export default {
  name: 'Login',
  data () {
    return {
      searchData: [],
      eachPageData: [],
      pageNum: 0,
      currentPage: 1
    }
  },
  components: {
    navigationBar
  },
  created () {
    this.currentPage = 1
    this.search(this.$route.params.type, this.$route.params.value)
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/search/' + this.$route.params.type + '/' + this.$route.params.value) {
        this.currentPage = 1
        this.search(this.$route.params.type, this.$route.params.value)
      }
    }
  },
  methods: {
    search (type, val) {
      var res
      this.$http.post(this.GLOBAL.baseUrl + 'api/backend/search', { type: type, val: val })
      .then((response) => {
        res = JSON.parse(response.bodyText)
        console.log(JSON.stringify(res))
        this.pageNum = (res.length / 6) * 10
        if (res.length === 0) {
          this.$route.params.type = 'none'
          this.searchData = []
        } else {
          this.searchData = res
          this.getEachPageData()
        }
      }).catch((response) => {
      })
    },
    getEachPageData () {
      var index, counts
      var len = this.searchData.length
      this.eachPageData.splice(0, this.eachPageData.length)
      for (index = (this.currentPage - 1) * 6, counts = 0; index < len; index++, counts++) {
        this.eachPageData.push(this.searchData[index])
        if (counts === 5) {
          break
        }
      }
    },
    clickCmpDetail (id) {
      this.$router.push('/competitiondetails/' + id)
    },
    clickGroDetail (user) {
      var mid = user.id
      var id = user.organizer_user.id
      this.$router.push('/otherUserPage/' + mid + '/' + id + '/1')
    },
    clickTotDetail (id) {
      this.$router.push('/tutorialDetails/' + id)
    },
    clickTalkDetail (id) {
      this.$router.push('/competitiondetails/' + id)
    },
    changePage (count) {
      this.currentPage = count
      this.getEachPageData()
    },
    stringCut (name) {
      if (name.length > 4) {
        var str = name.substring(0, 4)
        str += '...'
        return str
      } else {
        return name
      }
    }
  }
}
</script>

<style>
    .searchlayout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
    }
    .searchlayout-content{
        min-height: 200px;
        margin: 15px;
        padding: 50px;
        padding-top: 10px;
        padding-bottom:0px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
    }
    .searchlayout-content-main{
        padding: 10px;
    }
    .searchlayout-content-p{
        font-size: 15px;
        color: #9ea7b4;
    }
    .searchlayout-page{
        text-align: right;
        padding: 10px 40px 20px;
        
    }
    .searchlayout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
    .searchlayout-group-p{
        color: #657180;
        margin-left: 20px;
        word-break:break-all;
        word-wrap:break-word;
    }
    .searchlayout-group-img{
        width: 120px;
        height: 120px;
        border-radius: 120px;
        border: 3px solid #f5f7f9;
    }
</style>
