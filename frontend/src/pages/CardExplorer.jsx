import { useMemo, useState } from 'react'

import { getCardsCatalog } from '../core/api/cardsApi'
import { Badge } from '../components/ui/badge'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Input } from '../components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs'

const FILTERS = ['All', 'Cashback', 'Travel', 'Reward Points', 'Co-branded']

function CardExplorer() {
  const [query, setQuery] = useState('')
  const [filter, setFilter] = useState('All')
  const [cards] = useState(() => getCardsCatalog())

  const filteredCards = useMemo(() => {
    return cards.filter((card) => {
      const matchesFilter = filter === 'All' || card.rewardType === filter
      const q = query.trim().toLowerCase()
      const matchesQuery =
        q.length === 0 ||
        card.name.toLowerCase().includes(q) ||
        card.bestCategory.toLowerCase().includes(q) ||
        card.rewardType.toLowerCase().includes(q)

      return matchesFilter && matchesQuery
    })
  }, [cards, query, filter])

  return (
    <section className="space-y-6">
      <Card>
        <CardHeader className="p-5 pb-0">
          <CardTitle className="text-sm font-medium text-slate-300">Card Explorer</CardTitle>
        </CardHeader>
        <CardContent className="space-y-5 p-5">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
            <Input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search card name, reward type, category..."
              className="w-full lg:max-w-md"
            />
            <div className="flex flex-wrap gap-2">
              {FILTERS.map((chip) => (
                <Button
                  key={chip}
                  type="button"
                  variant={chip === filter ? 'secondary' : 'outline'}
                  className="h-9"
                  onClick={() => setFilter(chip)}
                >
                  {chip}
                </Button>
              ))}
            </div>
          </div>

          <Tabs defaultValue="table" className="w-full">
            <TabsList>
              <TabsTrigger value="table">Table View</TabsTrigger>
              <TabsTrigger value="compact">Compact View</TabsTrigger>
            </TabsList>

            <TabsContent value="table" className="mt-4">
              <div className="overflow-hidden rounded-2xl border border-slate-800">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Card Name</TableHead>
                      <TableHead>Reward Type</TableHead>
                      <TableHead>Annual Fee</TableHead>
                      <TableHead>Best Category</TableHead>
                      <TableHead className="text-right">Rating</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredCards.map((card) => (
                      <TableRow key={card.name}>
                        <TableCell className="font-medium text-slate-100">{card.name}</TableCell>
                        <TableCell>
                          <Badge variant="secondary">{card.rewardType}</Badge>
                        </TableCell>
                        <TableCell>{card.annualFee}</TableCell>
                        <TableCell>{card.bestCategory}</TableCell>
                        <TableCell className="text-right text-emerald-300">{card.rating.toFixed(1)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </TabsContent>

            <TabsContent value="compact" className="mt-4">
              <div className="grid grid-cols-1 gap-3 min-[1200px]:grid-cols-2">
                {filteredCards.map((card) => (
                  <Card key={card.name}>
                    <CardContent className="flex items-center justify-between p-5">
                      <div>
                        <div className="text-sm font-semibold text-slate-100">{card.name}</div>
                        <div className="mt-1 text-xs text-slate-400">{card.bestCategory}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-xs text-slate-500">Rating</div>
                        <div className="text-sm font-semibold text-emerald-300">{card.rating.toFixed(1)}</div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </section>
  )
}

export default CardExplorer
