import { Routes, Route, Navigate } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import Register from './pages/Register'
import Login from './pages/Login'
import ReferralLanding from './pages/ReferralLanding'
import Dashboard from './pages/Dashboard'
import OrderHistory from './pages/OrderHistory'
import AffiliateDashboard from './pages/AffiliateDashboard'
import ShopQueue from './pages/ShopQueue'
import PrintShopOnboarding from './pages/PrintShopOnboarding'
import PrintShopVerify from './pages/PrintShopVerify'
import Wallet from './pages/Wallet'
import ShopDetail from './pages/ShopDetail'
import OrderDetail from './pages/OrderDetail'
import AIDesigner from './pages/AIDesigner'
import AdminOrders from './pages/AdminOrders'
import AdminShops from './pages/AdminShops'
import AdminAccess from './pages/AdminAccess'
import AdminGate from './routes/AdminGate'
import KYC from './pages/KYC'
import ProtectedRoute from './routes/ProtectedRoute'
import Layout from './components/Layout'
import { useAuth } from './context/AuthContext'

function App() {
  const { user } = useAuth()

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/ref/:referral_code" element={<ReferralLanding />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/orders" element={<ProtectedRoute><OrderHistory /></ProtectedRoute>} />
        <Route path="/orders/:id" element={<ProtectedRoute><OrderDetail /></ProtectedRoute>} />
        <Route path="/wallet" element={<ProtectedRoute><Wallet /></ProtectedRoute>} />
        <Route path="/shop/:id" element={<ProtectedRoute><ShopDetail /></ProtectedRoute>} />
        <Route path="/design-studio" element={<ProtectedRoute><AIDesigner /></ProtectedRoute>} />
        <Route path="/affiliate/dashboard" element={<ProtectedRoute allowedRoles={['AMBASSADOR']}><AffiliateDashboard /></ProtectedRoute>} />
          <Route path="/affiliate/dashboard" element={<ProtectedRoute allowedRoles={['CUSTOMER']}><AffiliateDashboard /></ProtectedRoute>} />
        <Route path="/kyc" element={<ProtectedRoute><KYC /></ProtectedRoute>} />
        <Route path="/shop/queue" element={<ProtectedRoute allowedRoles={['PRINT_SHOP']}><ShopQueue /></ProtectedRoute>} />
        <Route path="/shop/onboard" element={<ProtectedRoute allowedRoles={['PRINT_SHOP']}><PrintShopOnboarding /></ProtectedRoute>} />
        <Route path="/shop/onboard/verify" element={<ProtectedRoute allowedRoles={['PRINT_SHOP']}><PrintShopVerify /></ProtectedRoute>} />
        <Route path="/admin" element={<AdminAccess />} />
        <Route path="/admin/orders" element={<AdminGate><AdminOrders /></AdminGate>} />
        <Route path="/admin/shops" element={<AdminGate><AdminShops /></AdminGate>} />
        <Route path="*" element={<Navigate to={user ? '/dashboard' : '/'} />} />
      </Routes>
    </Layout>
  )
}

export default App
