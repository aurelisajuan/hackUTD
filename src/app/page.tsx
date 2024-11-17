// 'use client'

// import { hydrateRoot } from 'react-dom/client';
// import { useState } from 'react'
// import { Eye, EyeOff, FileText, MessageSquare, UserCog, Search, User, BotIcon as Robot } from 'lucide-react'
// import { motion } from 'framer-motion'
// import logo from '../img/logo_dark.png'

// interface ChatMessage {
//   sender: string
//   message: string
//   timestamp: string
//   isAgent: boolean
// }

// interface Document {
//   id: string
//   name: string
//   type: string
//   status: 'urgent' | 'medium' | 'done'
// }

// interface UserInfo {
//   id: string
//   name: string
//   ssn: string
//   bankProfile: {
//     accountNumber: string
//     balance: string
//   }
// }

// export default function AdminDashboard() {
//   const [showSensitiveInfo, setShowSensitiveInfo] = useState(false)

//   const userInfo: UserInfo = {
//     // TODO: Replace with actual user data, backend
//     id: "USR12345",
//     name: "John Doe",
//     ssn: "123-45-6789",
//     bankProfile: {
//       accountNumber: "9876543210",
//       balance: "$10,000.00"
//     }
//   }

//   const chatTranscript: ChatMessage[] = [
//     // TODO: Replace with actual chat transcript, backend
//     { sender: "User", message: "Hi, I need help with my account.", timestamp: "10:00 AM", isAgent: false },
//     { sender: "Agent", message: "Hello! I'd be happy to help. Can you please verify your account number?", timestamp: "10:01 AM", isAgent: true },
//     { sender: "User", message: "Sure, it's 9876543210.", timestamp: "10:02 AM", isAgent: false },
//     { sender: "Agent", message: "Thank you. I see you have a question about your recent transaction. What would you like to know?", timestamp: "10:03 AM", isAgent: true }
//   ]

//   const documents: Document[] = [
//     // TODO: Replace with actual documents, backend
//     { id: "DOC001", name: "Account Statement", type: "PDF", status: 'urgent' },
//     { id: "DOC002", name: "Transaction Details", type: "PDF", status: 'medium' },
//     { id: "DOC003", name: "Dispute Form", type: "DOCX", status: 'done' }
//   ]

//   const maskSensitiveInfo = (info: string, isSSN = false) => {
//     return isSSN || !showSensitiveInfo ? info.replace(/\w/g, '*') : info;
//   }

//   return (
//     <div className="min-h-screen bg-[#000000] text-[#FFFFFF]">
//       {/* Navigation Bar */}
//       <nav className="border-b border-white/10 bg-[#000000]/80 backdrop-blur-xl">
//         <div className="mx-auto px-4 sm:px-6 lg:px-8">
//           <div className="flex h-16 items-center justify-between">
//             <div className="flex items-center">
//               <div className="flex items-center">
//                 <img src={logo.src} alt="Logo" className="h-12 w-12 mr-2" />
//                 <span className="text-xl font-semibold bg-gradient-to-r from-[#64A8F0] to-[#1c344e] bg-clip-text text-transparent">
//                   TalkTuahAI
//                 </span>
//               </div>
//             </div>
//             <div className="flex items-center gap-4">
//               <button className="px-4 py-2 text-sm text-[#FFFFFF]/70 hover:text-[#FFFFFF] transition-colors">
//                 Help
//               </button>
//               <button className="px-4 py-2 rounded-full bg-[#64A8F0] hover:bg-[#1c344e] transition-colors text-sm font-semibold">
//                 Sign Out
//               </button>
//             </div>
//           </div>
//         </div>
//       </nav>

//       <div className="container mx-auto px-4 py-8">
//         <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
//           {/* User Information Card */}
//           <motion.div
//             initial={{ opacity: 0, y: 20 }}
//             animate={{ opacity: 1, y: 0 }}
//             className="lg:col-span-1 rounded-xl bg-[#F5F5F5]/5 backdrop-blur-lg border border-white/10 overflow-hidden"
//           >
//             <div className="p-6">
//               <div className="flex justify-between items-center mb-6">
//                 <h2 className="text-xl font-semibold">User Information</h2>
//                 <button
//                   onClick={() => setShowSensitiveInfo(!showSensitiveInfo)}
//                   className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#64A8F0]/10 hover:bg-[#64A8F0]/20 text-[#64A8F0] text-sm transition-colors"
//                 >
//                   {showSensitiveInfo ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
//                   {showSensitiveInfo ? 'Hide' : 'Show'}
//                 </button>
//               </div>
//               <div className="space-y-4">
//                 <div>
//                   <label className="text-sm text-[#F5F5F5]">User ID</label>
//                   <p className="text-[#FFFFFF]">{userInfo.id}</p>
//                 </div>
//                 <div>
//                   <label className="text-sm text-[#F5F5F5]">Name</label>
//                   <p className="text-[#FFFFFF]">{userInfo.name}</p>
//                 </div>
//                 <div>
//                   <label className="text-sm text-[#F5F5F5]">SSN</label>
//                   <p className="text-[#FFFFFF]">{maskSensitiveInfo(userInfo.ssn, true)}</p>
//                 </div>
//                 <div>
//                   <label className="text-sm text-[#F5F5F5]">Account Number</label>
//                   <p className="text-[#FFFFFF]">{maskSensitiveInfo(userInfo.bankProfile.accountNumber)}</p>
//                 </div>
//                 <div>
//                   <label className="text-sm text-[#F5F5F5]">Balance</label>
//                   <p className="text-[#FFFFFF]">{userInfo.bankProfile.balance}</p>
//                 </div>
//               </div>
//             </div>
//           </motion.div>

//           {/* Chat Transcript Card */}
//           <motion.div
//             initial={{ opacity: 0, y: 20 }}
//             animate={{ opacity: 1, y: 0 }}
//             transition={{ delay: 0.1 }}
//             className="lg:col-span-2 rounded-xl bg-[#F5F5F5]/5 backdrop-blur-lg border border-white/10 overflow-hidden"
//           >
//             <div className="p-6">
//               <h2 className="text-xl font-semibold mb-6">Live Transcript</h2>
//               <div className="space-y-4 h-[400px] overflow-y-auto pr-4">
//               {chatTranscript.map((message, index) => (
//                 <div
//                   key={index}
//                   className={`p-4 rounded-lg ${
//                     message.isAgent
//                       ? 'bg-[#F5F5F5]/5 border border-white/10'
//                       : 'bg-[#64A8F0]/10 border border-[#64A8F0]/20'
//                   }`}
//                 >
//                   <div className="flex items-center gap-3 mb-2">
//                     <div className="w-8 h-8 rounded-full bg-[#64A8F0]/20 flex items-center justify-center">
//                       {message.isAgent ? (
//                         <Robot className="w-5 h-5 text-[#64A8F0]" />
//                       ) : (
//                         <User className="w-5 h-5 text-[#64A8F0]" />
//                       )}
//                     </div>
//                     <div>
//                       <span className="text-sm font-medium">{message.sender}</span>
//                       <span className="text-xs text-[#F5F5F5]/70 ml-2">{message.timestamp}</span>
//                     </div>
//                   </div>
//                   <p className="text-[#FFFFFF] ml-11">{message.message}</p>
//                 </div>
//               ))}
//             </div>
//               <motion.div
//                 initial={{ opacity: 0, y: 20 }}
//                 animate={{ opacity: 1, y: 0 }}
//                 transition={{ delay: 0.3 }}
//                 className="mt-4"
//               >
//                 <button className="px-4 py-2 text-sm bg-[#64A8F0] hover:bg-[#1c344e] transition-colors flex items-center justify-center gap-2 font-medium rounded-md">
//                   <UserCog className="h-5 w-5" />
//                   Transfer to Live Agent
//                 </button>
//               </motion.div>
//             </div>
//           </motion.div>

//           {/* Documents Card */}
//           <motion.div
//             initial={{ opacity: 0, y: 20 }}
//             animate={{ opacity: 1, y: 0 }}
//             transition={{ delay: 0.2 }}
//             className="lg:col-span-3 rounded-xl bg-[#F5F5F5]/5 backdrop-blur-lg border border-white/10 overflow-hidden"
//           >
//             <div className="p-6">
//               <h2 className="text-xl font-semibold mb-6">Referenced Documents</h2>
//               <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
//                 {documents.map((doc) => (
//                   <div
//                     key={doc.id}
//                     className="p-4 rounded-lg bg-[#F5F5F5]/5 border border-white/10 hover:border-[#64A8F0]/50 transition-colors"
//                   >
//                     <div className="flex items-start justify-between">
//                       <div>
//                         <h3 className="font-medium mb-1">{doc.name}</h3>
//                         <p className="text-sm text-[#F5F5F5]/70">{doc.type}</p>
//                       </div>
//                       <span
//                         className={`text-xs px-2 py-1 rounded-full ${
//                           doc.status === 'urgent'
//                             ? 'bg-red-500/10 text-red-500'
//                             : doc.status === 'medium'
//                             ? 'bg-yellow-500/10 text-yellow-500'
//                             : 'bg-green-500/10 text-green-500'
//                         }`}
//                       >
//                         {doc.status}
//                       </span>
//                     </div>
//                     <button className="mt-4 w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-[#64A8F0]/10 hover:bg-[#64A8F0]/20 text-[#64A8F0] transition-colors">
//                       <FileText className="h-4 w-4" />
//                       View Document
//                     </button>
//                   </div>
//                 ))}
//               </div>
//             </div>
//           </motion.div>
//         </div>
//       </div>

//       <style jsx global>{`
//         ::-webkit-scrollbar {
//           width: 8px;
//         }
//         ::-webkit-scrollbar-track {
//           background: rgba(255, 255, 255, 0.1);
//           border-radius: 10px;
//         }
//         ::-webkit-scrollbar-thumb {
//           background: rgba(255, 255, 255, 0.2);
//           border-radius: 10px;
//         }
//         ::-webkit-scrollbar-thumb:hover {
//           background: rgba(255, 255, 255, 0.3);
//         }
//       `}</style>
//     </div>
//   )
// }

// // Render the app
// const container = document.getElementById('root');
// if (container) {
//   // Use `hydrateRoot` if SSR is involved; otherwise, use `createRoot`.
//   if (container.hasChildNodes()) {
//     hydrateRoot(container, <AdminDashboard />);
//   } else {
//     hydrateRoot(container, <AdminDashboard />);
//   }
// }

'use client'

import { useState } from 'react'
import { Eye, EyeOff, FileText, MessageSquare, UserCog, Search, User, BotIcon as Robot, Menu } from 'lucide-react'
import { motion } from 'framer-motion'
import logo from '../img/logo_dark.png'

interface ChatMessage {
  sender: string
  message: string
  timestamp: string
  isAgent: boolean
}

interface Document {
  id: string
  name: string
  type: string
  status?: 'urgent' | 'medium' | 'done'
}

interface UserInfo {
  id: string
  name: string
  ssn: string
  bankProfile: {
    accountNumber: string
    balance: string
  }
}

const analyzeDocumentStatus = (doc: { name: string; type: string }): 'urgent' | 'medium' | 'done' => {
  if (doc.name.toLowerCase().includes('dispute')) return 'urgent';
  if (doc.type === 'PDF') return 'medium';
  return 'done';
};

export default function AdminDashboard() {
  const [showSensitiveInfo, setShowSensitiveInfo] = useState(false)
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const userInfo: UserInfo = {
    id: "USR12345",
    name: "John Doe",
    ssn: "123-45-6789",
    bankProfile: {
      accountNumber: "9876543210",
      balance: "$10,000.00"
    }
  }

  const chatTranscript: ChatMessage[] = [
    { sender: "User", message: "Hi, I need help with my account.", timestamp: "10:00 AM", isAgent: false },
    { sender: "Agent", message: "Hello! I'd be happy to help. Can you please verify your account number?", timestamp: "10:01 AM", isAgent: true },
    { sender: "User", message: "Sure, it's 9876543210.", timestamp: "10:02 AM", isAgent: false },
    { sender: "Agent", message: "Thank you. I see you have a question about your recent transaction. What would you like to know?", timestamp: "10:03 AM", isAgent: true }
  ]

  const documents: Document[] = [
    { id: "DOC001", name: "Account Statement", type: "PDF" },
    { id: "DOC002", name: "Transaction Details", type: "PDF" },
    { id: "DOC003", name: "Dispute Form", type: "DOCX" }
  ].map(doc => ({ ...doc, status: analyzeDocumentStatus(doc) }));

  const maskSensitiveInfo = (info: string, isSSN = false) => {
    return !showSensitiveInfo ? info.replace(/\w/g, '*') : info;
  }

  return (
    <div className="min-h-screen bg-[#000000] text-[#FFFFFF]">
      {/* Navigation Bar */}
      <nav className="border-b border-white/10 bg-[#000000]/80 backdrop-blur-xl">
        <div className="mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center cursor-pointer" onClick={() => setIsMenuOpen(!isMenuOpen)}>
              {/* <Menu className="h-6 w-6 mr-2 text-[#64A8F0]" /> */}
              <img src={logo.src} alt="Logo" className="h-12 w-12 mr-2" />
              <span className="text-xl font-semibold bg-gradient-to-r from-[#64A8F0] to-[#1c344e] bg-clip-text text-transparent">
                TalkTuahAI
              </span>
            </div>
            <div className="flex items-center gap-4">
              <button className="px-4 py-2 text-sm text-[#FFFFFF]/70 hover:text-[#FFFFFF] transition-colors">
                Help
              </button>
              <button className="px-4 py-2 rounded-full bg-[#64A8F0] hover:bg-[#4A86C8] transition-colors text-sm font-medium">
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex">
        {/* Side Menu */}
        <div className={`fixed left-0 top-16 h-full bg-[#000000] border-r border-white/10 overflow-y-auto transition-all duration-300 ${isMenuOpen ? 'w-64' : 'w-0'}`}>
          <div className="p-4">
            <h3 className="text-lg font-semibold mb-4">Previous Messages</h3>
            <ul className="space-y-2">
              <li className="p-2 hover:bg-[#F5F5F5]/5 rounded cursor-pointer">Previous message 1</li>
              <li className="p-2 hover:bg-[#F5F5F5]/5 rounded cursor-pointer">Previous message 2</li>
              <li className="p-2 hover:bg-[#F5F5F5]/5 rounded cursor-pointer">Previous message 3</li>
            </ul>
          </div>
        </div>

        {/* Main Content */}
        <div className={`flex-1 transition-all duration-300 ${isMenuOpen ? 'ml-64' : 'ml-0'}`}>
          <div className="container mx-auto px-4 py-8">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* User Information Card */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`lg:col-span-1 rounded-xl bg-[#F5F5F5]/5 backdrop-blur-lg border border-white/10 overflow-hidden ${isMenuOpen ? 'lg:col-span-3 xl:col-span-1' : ''}`}
              >
                <div className="p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-lg font-semibold">User Information</h2>
                    <button
                      onClick={() => setShowSensitiveInfo(!showSensitiveInfo)}
                      className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#64A8F0]/10 hover:bg-[#64A8F0]/20 text-[#64A8F0] text-sm transition-colors"
                    >
                      {showSensitiveInfo ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      {showSensitiveInfo ? 'Hide' : 'Show'}
                    </button>
                  </div>
                  <div className={`grid ${isMenuOpen ? 'grid-cols-2 xl:grid-cols-1 gap-4' : 'space-y-4'}`}>
                    <div>
                      <label className="text-sm text-[#F5F5F5]">User ID</label>
                      <p className="text-[#FFFFFF]">{userInfo.id}</p>
                    </div>
                    <div>
                      <label className="text-sm text-[#F5F5F5]">Name</label>
                      <p className="text-[#FFFFFF]">{userInfo.name}</p>
                    </div>
                    <div>
                      <label className="text-sm text-[#F5F5F5]">SSN</label>
                      <p className="text-[#FFFFFF]">{maskSensitiveInfo(userInfo.ssn, true)}</p>
                    </div>
                    <div>
                      <label className="text-sm text-[#F5F5F5]">Account Number</label>
                      <p className="text-[#FFFFFF]">{maskSensitiveInfo(userInfo.bankProfile.accountNumber)}</p>
                    </div>
                    <div>
                      <label className="text-sm text-[#F5F5F5]">Balance</label>
                      <p className="text-[#FFFFFF]">{userInfo.bankProfile.balance}</p>
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* Chat Transcript Card */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className={`lg:col-span-2 rounded-xl bg-[#F5F5F5]/5 backdrop-blur-lg border border-white/10 overflow-hidden ${isMenuOpen ? 'lg:col-span-3 xl:col-span-2' : ''}`}
              >
                <div className="p-6">
                  <h2 className="text-lg font-semibold mb-6">Chat Transcript</h2>
                  <div className="space-y-4 h-[400px] overflow-y-auto pr-4">
                    {chatTranscript.map((message, index) => (
                      <div
                        key={index}
                        className={`p-4 rounded-lg ${
                          message.isAgent
                            ? 'bg-[#F5F5F5]/5 border border-white/10'
                            : 'bg-[#64A8F0]/10 border border-[#64A8F0]/20'
                        }`}
                      >
                        <div className="flex items-center gap-3 mb-2">
                          <div className="w-8 h-8 rounded-full bg-[#64A8F0]/20 flex items-center justify-center">
                            {message.isAgent ? (
                              <Robot className="w-5 h-5 text-[#64A8F0]" />
                            ) : (
                              <User className="w-5 h-5 text-[#64A8F0]" />
                            )}
                          </div>
                          <div>
                            <span className="text-sm font-medium">{message.sender}</span>
                            <span className="text-xs text-[#F5F5F5]/70 ml-2">{message.timestamp}</span>
                          </div>
                        </div>
                        <p className="text-[#FFFFFF] ml-11">{message.message}</p>
                      </div>
                    ))}
                  </div>
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="mt-4"
                  >
                    <button className="px-4 py-2 text-sm bg-[#64A8F0] hover:bg-[#4A86C8] transition-colors flex items-center justify-center gap-2 font-medium rounded-md">
                      <UserCog className="h-5 w-5" />
                      Transfer to Live Agent
                    </button>
                  </motion.div>
                </div>
              </motion.div>

              {/* Documents Card */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="lg:col-span-3 rounded-xl bg-[#F5F5F5]/5 backdrop-blur-lg border border-white/10 overflow-hidden"
              >
                <div className="p-6">
                  <h2 className="text-lg font-semibold mb-6">Referenced Documents</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {documents.map((doc) => (
                      <div
                        key={doc.id}
                        className="p-4 rounded-lg bg-[#F5F5F5]/5 border border-white/10 hover:border-[#64A8F0]/50 transition-colors"
                      >
                        <div className="flex items-start justify-between">
                          <div>
                            <h3 className="font-medium mb-1">{doc.name}</h3>
                            <p className="text-sm text-[#F5F5F5]/70">{doc.type}</p>
                          </div>
                          <span
                            className={`text-xs px-2 py-1 rounded-full ${
                              doc.status === 'urgent'
                                ? 'bg-red-500/10 text-red-500'
                                : doc.status === 'medium'
                                ? 'bg-yellow-500/10 text-yellow-500'
                                : 'bg-green-500/10 text-green-500'
                            }`}
                          >
                            {doc.status}
                          </span>
                        </div>
                        <button className="mt-4 w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-[#64A8F0]/10 hover:bg-[#64A8F0]/20 text-[#64A8F0] transition-colors">
                          <FileText className="h-4 w-4" />
                          View Document
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </div>
      </div>

      <style jsx global>{`
        ::-webkit-scrollbar {
          width: 8px;
        }
        ::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.2);
          border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background: rgba(255, 255, 255, 0.3);
        }
      `}</style>
    </div>
  )
}