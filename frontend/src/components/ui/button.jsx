import * as React from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva } from 'class-variance-authority'
import { motion } from 'framer-motion'

import { cn } from '../../lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center whitespace-nowrap rounded-[10px] text-sm font-semibold ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500/50 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:brightness-110',
  {
    variants: {
      variant: {
        default: 'bg-indigo-500 text-white hover:bg-indigo-400',
        secondary: 'bg-slate-800 text-slate-100 hover:bg-slate-700',
        ghost: 'bg-transparent text-slate-300 hover:bg-slate-800/70 hover:text-slate-100',
        outline: 'border border-white/10 bg-slate-900/60 text-slate-100 hover:bg-slate-800/60',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  },
)

const Button = React.forwardRef(({ className, variant, size, asChild = false, ...props }, ref) => {
  if (asChild) {
    return <Slot className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
  }

  return <motion.button whileTap={{ scale: 0.97 }} className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
})
Button.displayName = 'Button'

export { Button, buttonVariants }
