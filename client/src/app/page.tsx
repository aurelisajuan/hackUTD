'use client'

import { useState, useEffect } from 'react'
import { Eye, EyeOff, FileText, UserCog, User, BotIcon as Robot, ChevronDown } from 'lucide-react'
import { motion } from 'framer-motion'
import logo from '../img/logo_dark.png'

interface ChatMessage {
  role: string,
  content: string
}

interface CallResponse {
  event: "calls_response";
  data: Record<string, Call>;
}

interface Call {
  id: string
  transcript: ChatMessage[]
  referenced_documents: Document[]
  user_id: string
}

interface DBResponse {
  event: "db_response";
  data: Database;
}

interface CombinedResponse {
  event: "combined_response";
  calls: Record<string, Call>;
  db: Database;
}

interface Database {
  users: {
    [key: string]: {
      name: string
      accounts: string[]
      ssn: string
      address: string
      date_of_birth: string
      email: string
      phone: string
    }
  }
  accounts: {
    [key: string]: {
      balance: number
      statements: {
        [month: string]: string
      }
    }
  }
  payments: {
    [key: string]: {
      from_account: string
      to_account: string
      amount: number
      date: string
      status: string
    }
  }
}

export interface CallProps {
  call?: Call;
  selectedId: string | undefined;
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
  address: string
  date_of_birth: string
  email: string
  phone: string
}

interface Transaction {
  id: string
  date: string
  description: string
  amount: string
}

const analyzeDocumentStatus = (doc: { name: string; type: string }): 'urgent' | 'medium' | 'done' => {
  if (doc.name.toLowerCase().includes('dispute')) return 'urgent';
  if (doc.type === 'PDF') return 'medium';
  return 'done';
};

export default function AdminDashboard() {
  const [showSensitiveInfo, setShowSensitiveInfo] = useState(false)
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState('info');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [connected, setConnected] = useState(false);
  const [data, setData] = useState<Record<string, Call>>({});
  const [selectedId, setSelectedId] = useState<string>("");
  const [bankData, setBankData] = useState<Database>({
    users: {},
    accounts: {},
    payments: {}
  });
  const [socket, setSocket] = useState(null)
  const [userInfo, setUserInfo] = useState<UserInfo>({
    id: "",
    name: "",
    ssn: "",
    bankProfile: {
      accountNumber: "",
      balance: ""
    }
  });

  const [transactions, setTransactions] = useState<Transaction[]>([]);

  useEffect(() => {
    const wss = new WebSocket(
      "ws://localhost:8000/ws?client_id=1234",
    );
    console.log("useEffect")
    wss.onopen = () => {
      console.log('WebSocket connection established')
      setConnected(true)
    }

    wss.onmessage = (event: MessageEvent) => {
      console.log("Received message");
      const data = JSON.parse(event.data)
      console.log(data)
      if (data.event === "combined_response") {
        setData(data.calls)
        setBankData(data.db)
      }
      else if (data.event === "db_response") {
        setBankData(data.data)
      }
      else if (data.event === "calls_response") {
        setData(data.data)
      }
    }

    setSocket(wss)
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(
          JSON.stringify({
            event: "get_all_dbs",
          })
        );
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [socket]);

  const handleCallSelect = (id: string) => {
    setSelectedId(id);
    const selectedCall = data[id];
    if (selectedCall && bankData.users && bankData.users[selectedCall.user_id]) {
      const user = bankData.users[selectedCall.user_id];
      const userAccounts = user.accounts.map(accId => {
        const account = bankData.accounts[accId];
        return {
          accountNumber: accId,
          balance: account ? `$${account.balance.toFixed(2)}` : "N/A"
        };
      });

      // Update user info
      setUserInfo({
        id: selectedCall.user_id,
        name: user.name,
        ssn: user.ssn,
        address: user.address,
        date_of_birth: user.date_of_birth,
        email: user.email,
        phone: user.phone
      });

      // Update transactions from payments
      const userTransactions: Transaction[] = Object.entries(bankData.payments)
        .filter(([_, payment]) =>
          payment.from_account === userAccounts[0]?.accountNumber ||
          payment.to_account === userAccounts[0]?.accountNumber
        )
        .map(([id, payment]) => ({
          id,
          date: payment.date,
          description: `${payment.from_account === userAccounts[0]?.accountNumber ? 'Payment to' : 'Payment from'} ${payment.from_account === userAccounts[0]?.accountNumber ? payment.to_account : payment.from_account
            }`,
          amount: `${payment.from_account === userAccounts[0]?.accountNumber ? '-' : '+'}$${payment.amount.toFixed(2)}`
        }));

      setTransactions(userTransactions);
    }
  };

  const maskSensitiveInfo = (info: string) => {
    if (!info) return '';
    return !showSensitiveInfo ? info.replace(/\d/g, '*') : info;
  }

  return (
    <div className="min-h-screen bg-[#000000] text-[#FFFFFF]">
      {/* Navigation Bar */}
      <nav className="border-b border-white/10 bg-[#000000]/80 backdrop-blur-xl">
        <div className="mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center cursor-pointer" onClick={() => setIsMenuOpen(!isMenuOpen)}>
              <img src={logo.src} alt="Logo" className="h-12 w-12 mr-2" />
              <span className="text-xl font-semibold bg-gradient-to-r from-[#64A8F0] to-[#1c344e] bg-clip-text text-transparent">
                TalkTuahBank
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
              {data && Object.entries(data).map(([id, call]) => (
                <li
                  key={id}
                  className={`p-2 hover:bg-[#F5F5F5]/5 rounded cursor-pointer ${selectedId === id ? 'bg-[#64A8F0]/10' : ''}`}
                  onClick={() => handleCallSelect(id)}
                >
                  {call.id}
                </li>
              ))}
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
                    <div className="relative">
                      <button
                        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                        className="flex items-center gap-2 text-lg font-semibold focus:outline-none"
                      >
                        {selectedOption === 'info' ? 'User Information' : 'User Transactions'}
                        <ChevronDown className="h-4 w-4" />
                      </button>
                      {isDropdownOpen && (
                        <div className="absolute z-10 mt-2 w-56 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5">
                          <div className="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
                            <button
                              onClick={() => {
                                setSelectedOption('info');
                                setIsDropdownOpen(false);
                              }}
                              className="block px-4 py-2 text-sm text-gray-700 hover:bg-[#64A8F0] hover:text-gray-900 w-full text-left"
                              role="menuitem"
                            >
                              User Information
                            </button>
                            <button
                              onClick={() => {
                                setSelectedOption('transactions');
                                setIsDropdownOpen(false);
                              }}
                              className="block px-4 py-2 text-sm text-gray-700 hover:bg-[#64A8F0] hover:text-gray-900 w-full text-left"
                              role="menuitem"
                            >
                              User Transactions
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                    <button
                      onClick={() => setShowSensitiveInfo(!showSensitiveInfo)}
                      className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#64A8F0]/10 hover:bg-[#64A8F0]/20 text-[#64A8F0] text-sm transition-colors"
                    >
                      {showSensitiveInfo ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      {showSensitiveInfo ? 'Hide' : 'Show'}
                    </button>
                  </div>
                  {selectedOption === 'info' ? (
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
                        <p className="text-[#FFFFFF]">{maskSensitiveInfo(userInfo.ssn)}</p>
                      </div>
                      <div>
                        <label className="text-sm text-[#F5F5F5]">Address</label>
                        <p className="text-[#FFFFFF]">{userInfo.address}</p>
                      </div>
                      <div>
                        <label className="text-sm text-[#F5F5F5]">Date Of Birth</label>
                        <p className="text-[#FFFFFF]">{userInfo.date_of_birth}</p>
                      </div>
                      <div>
                        <label className="text-sm text-[#F5F5F5]">Email</label>
                        <p className="text-[#FFFFFF]">{userInfo.email}</p>
                      </div>
                      <div>
                        <label className="text-sm text-[#F5F5F5]">Phone Number</label>
                        <p className="text-[#FFFFFF]">{userInfo.phone}</p>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {transactions.map((transaction) => (
                        <div key={transaction.id} className="flex justify-between items-center p-2 rounded bg-[#F5F5F5]/10">
                          <div>
                            <p className="text-sm font-medium">{transaction.description}</p>
                            <p className="text-xs text-[#F5F5F5]/70">{transaction.date}</p>
                          </div>
                          <p className={`text-sm font-medium ${transaction.amount.startsWith('+') ? 'text-green-500' : 'text-red-500'}`}>
                            {transaction.amount}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
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
                    {selectedId && data[selectedId] ? (
                      data[selectedId].transcript.map((message, index) => (
                        <div
                          key={index}
                          className={`p-4 rounded-lg ${message.role === 'assistant'
                            ? 'bg-[#F5F5F5]/5 border border-white/10'
                            : 'bg-[#64A8F0]/10 border border-[#64A8F0]/20'
                            }`}
                        >
                          <div className="flex items-center gap-3 mb-2">
                            <div className="w-8 h-8 rounded-full bg-[#64A8F0]/20 flex items-center justify-center">
                              {message.role === 'assistant' ? (
                                <Robot className="w-5 h-5 text-[#64A8F0]" />
                              ) : (
                                <User className="w-5 h-5 text-[#64A8F0]" />
                              )}
                            </div>
                            <div>
                              <span className="text-sm font-medium">{message.role}</span>
                            </div>
                          </div>
                          <p className="text-[#FFFFFF] ml-11">{message.content}</p>
                        </div>
                      ))
                    ) : (
                      <div className="text-center text-[#F5F5F5]/70">
                        Select a conversation from the sidebar to view the transcript
                      </div>
                    )}
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
                    {selectedId && data[selectedId] ? (
                      data[selectedId].referenced_documents.map((doc) => (
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
                              className={`text-xs px-2 py-1 rounded-full ${doc.status === 'urgent'
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
                      ))
                    ) : (
                      <div className="col-span-3 text-center text-[#F5F5F5]/70">
                        Select a conversation to view referenced documents
                      </div>
                    )}
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