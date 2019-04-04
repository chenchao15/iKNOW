<script>
  // var baseUrl = 'http://118.89.240.107/'
  var baseUrl = 'http://127.0.0.1:8000/'
  var priUserId = -1
  var userType = -1
  var orgUserId = -1
  var curChatName = ''
  var curChatTime = ''
  var curChatContent = ''
  var orgInfoForm = {
    name: '',
    abbreviation: '',
    briefintro: '',
    address: '',
    field: '',
    linkman: '',
    phonenumber: '',
    contact_email: '',
    file_name: '',
    file_url: ''
  }
  var priInfoForm = {
    name: '',
    nickname: '',
    phone_number: '',
    gender: '',
    school: '',
    major: '',
    student_number: '',
    introduction: ''
  }
  var avatarUrl = ''
  var competitionType = -1
  var islogin = 0
  var competitionId = -1
  var competeBasicInfo = {
    id: -1,
    name: '',
    sponsor: '',
    othersponsor: [''],
    otherorganizer: [''],
    organizer: '',
    objectrange: '',
    objectschool: '',
    otherobjectschool: [''],
    level: '',
    detail: '',
    imageurl: ''
  }
  export default
  {
    priUserId,
    userType,
    orgUserId,
    orgInfoForm,
    priInfoForm,
    competitionType,
    islogin,
    baseUrl,
    curChatName,
    curChatTime,
    curChatContent,
    avatarUrl,
    competeBasicInfo,
    competitionId
  }
</script>
