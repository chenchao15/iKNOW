import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import Search from '@/views/Search'
import Signup from '@/views/SignUp'
import Login from '@/views/Login'
import PriPage from '@/views/PriPage'
import OrgPage from '@/views/OrgPage'
import ModifyOrgInfo from '@/views/ModifyOrgInfo'
import ModifyPriInfo from '@/views/ModifyPriInfo'
import TutorialDetails from '@/views/TutorialDetails'
import OfficialTutorial from '@/views/OfficialTutorial'
import StudentShare from '@/views/StudentShare'
import CompetitionHomepage from '@/views/CompetitionHomepage'
import CompetitionDetails from '@/views/CompetitionDetails'
import CompetitionManage from '@/views/CompetitionManage'
import ValidateEmail from '@/views/ValidateEmail'
import RegisterPage from '@/views/RegisterPage'
import ForgetPwd from '@/views/ForgetPwd'
import ResetPwd from '@/views/ResetPwd'
import CreateCompetition from '@/views/CreateCompetition'
import ModifyCompetitionBasic from '@/views/ModifyCompetitionBasic'
import NoticeDetails from '@/views/NoticeDetails'
import CreateNotice from '@/views/CreateNotice'
import EditNotice from '@/views/EditNotice'
import GroupMessageDetails from '@/views/GroupMessageDetails'
import CreateGroupMessage from '@/views/CreateGroupMessage'
import EditGroupMessage from '@/views/EditGroupMessage'
import OtherUserPage from '@/views/OtherUserPage'
import ManagerLogin from '@/views/ManagerLogin'
import Manager from '@/views/Manager'
import Agreement from '@/views/Agreement'
import AllCompetitions from '@/views/AllCompetitions'
import AllTutorials from '@/views/AllTutorials'
import CreateTutorial from '@/views/CreateTutorial'
import ModifyTutorial from '@/views/ModifyTutorial'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/admin',
      component: Manager
    },
    {
      path: '/adminLogin',
      component: ManagerLogin
    },
    {
      path: '/home',
      component: Home
    },
    {
      path: '/search/:type/:value',
      component: Search
    },
    {
      path: '/signup',
      component: Signup
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/pripage',
      component: PriPage
    },
    {
      path: '/orgpage',
      component: OrgPage
    },
    {
      path: '/modify_pri_info',
      component: ModifyPriInfo
    },
    {
      path: '/modify_org_info',
      component: ModifyOrgInfo
    },
    {
      path: '/tutorialDetails/:id',
      component: TutorialDetails
    },
    {
      path: '/officialTutorial',
      component: OfficialTutorial
    },
    {
      path: '/studentShare',
      component: StudentShare
    },
    {
      path: '/validate_email/:encode_id',
      component: ValidateEmail
    },
    {
      path: '/forget_password',
      component: ForgetPwd
    },
    {
      path: '/change_password/:encode_id',
      component: ResetPwd
    },
    {
      path: '/competitionhomepage/:id',
      component: CompetitionHomepage
    },
    {
      path: '/registerpage/:comid/:stageid',
      component: RegisterPage
    },
    {
      path: '/competitiondetails/:id',
      component: CompetitionDetails
    },
    {
      path: '/createcompetition',
      component: CreateCompetition
    },
    {
      path: '/modifycompetitionbasic/:id',
      component: ModifyCompetitionBasic
    },
    {
      path: '/competitionmanage/:id',
      component: CompetitionManage
    },
    {
      path: '/noticeDetails/:id',
      component: NoticeDetails
    },
    {
      path: '/createNotice/:id',
      component: CreateNotice
    },
    {
      path: '/editNotice/:competition_id/:id',
      component: EditNotice
    },
    {
      path: '/createGroupMessage/:id',
      component: CreateGroupMessage
    },
    {
      path: '/editGroupMessage/:competition_id/:id',
      component: EditGroupMessage
    },
    {
      path: '/groupMessageDetails/:id',
      component: GroupMessageDetails
    },
    {
      path: '/otherUserPage/:mid/:id/:type',
      component: OtherUserPage
    },
    {
      path: '/competitions',
      component: AllCompetitions
    },
    {
      path: '/createtutorial',
      component: CreateTutorial
    },
    {
      path: '/modifytutorial/:id',
      component: ModifyTutorial
    },
    {
      path: '/tutorials',
      component: AllTutorials
    },
    {
      path: '/agreement',
      component: Agreement
    }
  ]
})
