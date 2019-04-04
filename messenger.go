package main

import (
	"fmt"
	"strings"
	"os"
	"os/exec"
	"runtime"
	"bufio"
	"os/signal"
	"syscall"
	"net"
	"reflect"
	"sync"
	"github.com/msgpack-rpc/msgpack-rpc-go/rpc"
)

type Resolver map[string]reflect.Value

func connect(ip string, port int) (bool, fmt.Stringer){

	return true, nil
}
func connectSuccess(ip string, port int) (bool, fmt.Stringer){

	return true, nil
}


