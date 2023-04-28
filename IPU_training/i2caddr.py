from machine import I2C
i2c=I2C(2,I2C.MASTER,baudrate=100000)
  
#ir_1=MLX90614(i2c, addr=0x5A)


def changeDirec (OldDirec, NewDirec):
    #print(i2c.mem_write( 0x2E ,OldDirec, 0X0E))                # send command for device to return address 
    
    print('before:', i2c.mem_read(10, 0x5A, 0x0E, timeout  = 20000))
    i2c.mem_write( 0x00 ,OldDirec, 0x0E ,timeout  =20000)                  # send zeros to erase                 
    
 
              
    i2c.mem_write(0x5B, OldDirec, 0x0E, timeout  =20000)           
    print('after:', i2c.mem_read(10, 0x5A, 0x0E, timeout  = 20000))
    #print('ok')


changeDirec ( 0x5A , 0x2A )