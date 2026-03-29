import { Body, Controller, Post } from '@nestjs/common'
import axios from 'axios'

@Controller('cards')
export class CardsController {
  @Post('optimize')
  async optimize(@Body() spend: any) {
    const res = await axios.post('http://localhost:8001/optimize-spend', spend)
    return res.data
  }
}
