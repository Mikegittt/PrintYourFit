import { useState, useEffect } from 'react'
import api from '../services/api'
import LoadingButton from '../components/LoadingButton'
import { useToast } from '../context/ToastContext'

export default function AIDesigner() {
  const [prompt, setPrompt] = useState('')
  const [designs, setDesigns] = useState([])
  const [loading, setLoading] = useState(false)
  const [exporting, setExporting] = useState(null)
  const [selectedDesign, setSelectedDesign] = useState(null)
  const [shops, setShops] = useState([])
  const [selectedShop, setSelectedShop] = useState(null)
  const { showToast } = useToast()

  useEffect(() => {
    loadDesigns()
    loadShops()
  }, [])

  async function loadDesigns() {
    try {
      const res = await api.get('/designs/my-designs')
      const list = res.data || []
      setDesigns(list)
      if (list.length && !selectedDesign) {
        setSelectedDesign(list[0])
      }
    } catch (e) {
      // ignore
    }
  }

  async function loadShops() {
    try {
      const res = await api.get('/print-shops/discover')
      setShops(res.data || [])
    } catch (e) {
      // ignore
    }
  }

  async function generateDesign() {
    if (!prompt.trim()) {
      showToast({ message: 'Enter a design prompt', type: 'error' })
      return
    }
    setLoading(true)
    try {
      const res = await api.post('/designs/generate', { prompt })
      setDesigns([res.data, ...designs])
      setSelectedDesign(res.data)
      setPrompt('')
      showToast({ message: 'Design generated!', type: 'success' })
    } catch (e) {
      showToast({ message: e.response?.data?.detail || 'Design generation failed', type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  async function exportDesign(format) {
    if (!selectedDesign) return
    setExporting(format)
    try {
      const res = await api.post(`/designs/${selectedDesign.id}/export`, { format }, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `design.${format.toLowerCase()}`)
      document.body.appendChild(link)
      link.click()
      link.parentNode.removeChild(link)
      showToast({ message: `Design exported as ${format}`, type: 'success' })
    } catch (e) {
      showToast({ message: 'Export failed', type: 'error' })
    } finally {
      setExporting(null)
    }
  }

  async function sendToPrinter() {
    if (!selectedDesign) {
      showToast({ message: 'Select a design first', type: 'error' })
      return
    }
    if (!selectedShop) {
      showToast({ message: 'Select a printer first', type: 'error' })
      return
    }
    try {
      await api.post(`/designs/${selectedDesign.id}/send-to-printer`, {
        printer_id: selectedShop.id,
        printer_name: selectedShop.shop_name,
      })
      showToast({ message: 'Design sent to printer for negotiation!', type: 'success' })
    } catch (e) {
      showToast({ message: e.response?.data?.detail || 'Failed to send design', type: 'error' })
    }
  }

  return (
    <div className="space-y-6">
      <section className="glass-card p-6">
        <p className="text-sm uppercase tracking-[0.24em] text-indigo-200">AI Design Assistant</p>
        <h1 className="mt-2 text-3xl font-semibold text-white">Create custom designs</h1>
        <p className="mt-2 text-slate-300">Describe your design idea in detail, and our AI will generate it for you.</p>
      </section>

      <div className="grid gap-6 lg:grid-cols-[1.75fr_1fr]">
        <div className="space-y-6">
          <section className="glass-card p-6">
            <label className="text-sm font-medium text-slate-200">Your design prompt</label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the design you want: colors, style, elements, mood, etc."
              className="mt-3 w-full h-32 rounded-lg bg-slate-900/60 px-4 py-3 text-slate-200"
            />
            <LoadingButton
              onClick={generateDesign}
              loading={loading}
              className="mt-4 bg-indigo-500 text-white w-full"
            >
              {loading ? 'Generating…' : 'Generate Design'}
            </LoadingButton>
          </section>

          {selectedDesign && (
            <section className="glass-card p-6">
              <p className="text-sm uppercase tracking-[0.24em] text-cyan-200">Generated Design</p>
              <div className="mt-4 rounded-lg overflow-hidden bg-slate-950/60">
                  {selectedDesign.image_url ? (
                    <img src={selectedDesign.image_url} alt="Generated design" className="w-full h-[320px] object-cover" />
                  ) : (
                    <div className="flex min-h-[240px] items-center justify-center border border-dashed border-slate-700 text-slate-500">
                      No preview available
                    </div>
                  )}
                </div>
                <p className="mt-4 text-sm text-slate-400 font-mono break-words">{selectedDesign.prompt}</p>

                <div className="mt-6 space-y-3">
                  <p className="text-sm font-medium text-slate-200">Export as:</p>
                  <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
                  {['PNG', 'JPEG', 'WebP', 'SVG'].map((fmt) => (
                    <LoadingButton
                      key={fmt}
                      onClick={() => exportDesign(fmt)}
                      loading={exporting === fmt}
                      className="w-full text-xs bg-slate-800/70 text-white"
                    >
                      {fmt}
                    </LoadingButton>
                  ))}
                </div>
              </div>
            </section>
          )}
        </div>

        <div className="space-y-6">
          <section className="glass-card p-6">
            <p className="text-sm uppercase tracking-[0.24em] text-rose-200">Recent Designs</p>
            <div className="mt-4 space-y-2 max-h-96 overflow-y-auto">
              {designs.length === 0 && (
                <div className="rounded-3xl border border-dashed border-slate-800/60 bg-slate-900/80 p-5 text-slate-400">
                  No designs yet. Use the prompt above to generate a custom print design.
                </div>
              )}
              {designs.map((d) => (
                <button
                  key={d.id}
                  onClick={() => setSelectedDesign(d)}
                  className={`w-full p-3 rounded-lg text-left text-sm ${
                    selectedDesign?.id === d.id
                      ? 'bg-indigo-500/30 border border-indigo-500'
                      : 'bg-slate-900/60 border border-slate-800/60 hover:border-slate-700'
                  }`}
                >
                  <p className="font-medium text-slate-100 truncate">{d.prompt.substring(0, 50)}</p>
                  <p className="text-xs text-slate-400 mt-1">{new Date(d.created_at).toLocaleDateString()}</p>
                </button>
              ))}
            </div>
          </section>

          {selectedDesign && (
            <section className="glass-card p-6">
              <p className="text-sm uppercase tracking-[0.24em] text-cyan-200">Send to Printer</p>
              <div className="mt-4 space-y-3">
                <select
                  value={selectedShop?.id ? String(selectedShop.id) : ''}
                  onChange={(e) => setSelectedShop(shops.find((s) => String(s.id) === e.target.value))}
                  className="w-full rounded-lg bg-slate-900/60 px-3 py-2 text-slate-200 text-sm"
                >
                  <option value="">Select a printer…</option>
                  {shops.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.shop_name} · {s.state}
                    </option>
                  ))}
                </select>
                {shops.length === 0 && (
                  <p className="text-sm text-slate-400">No printers available yet. Check back after onboarding print shops.</p>
                )}
                <LoadingButton onClick={sendToPrinter} className="w-full bg-rose-500 text-white text-sm">
                  Send for Negotiation
                </LoadingButton>
              </div>
            </section>
          )}
        </div>
      </div>
    </div>
  )
}
