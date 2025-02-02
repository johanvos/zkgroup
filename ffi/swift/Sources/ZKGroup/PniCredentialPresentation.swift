//
// Copyright (C) 2020 Signal Messenger, LLC.
// All rights reserved.
//
// SPDX-License-Identifier: GPL-3.0-only
//
// Generated by zkgroup/codegen/codegen.py - do not edit

import Foundation
import libzkgroup

public class PniCredentialPresentation : ByteArray {

  public static let SIZE: Int = 841

  public init(contents: [UInt8]) throws  {
    try super.init(newContents: contents, expectedLength: PniCredentialPresentation.SIZE)

    
    let ffi_return = FFI_PniCredentialPresentation_checkValidContents(self.contents, UInt32(self.contents.count))

    if (ffi_return == Native.FFI_RETURN_INPUT_ERROR) {
      throw ZkGroupException.InvalidInput
    }

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }
  }

  public func getAciCiphertext() throws  -> UuidCiphertext {
    var newContents: [UInt8] = Array(repeating: 0, count: UuidCiphertext.SIZE)

    let ffi_return = FFI_PniCredentialPresentation_getAciCiphertext(self.contents, UInt32(self.contents.count), &newContents, UInt32(newContents.count))

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }

    do {
      return try UuidCiphertext(contents: newContents)
    } catch ZkGroupException.InvalidInput {
      throw ZkGroupException.AssertionError
    }

  }

  public func getPniCiphertext() throws  -> UuidCiphertext {
    var newContents: [UInt8] = Array(repeating: 0, count: UuidCiphertext.SIZE)

    let ffi_return = FFI_PniCredentialPresentation_getPniCiphertext(self.contents, UInt32(self.contents.count), &newContents, UInt32(newContents.count))

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }

    do {
      return try UuidCiphertext(contents: newContents)
    } catch ZkGroupException.InvalidInput {
      throw ZkGroupException.AssertionError
    }

  }

  public func getProfileKeyCiphertext() throws  -> ProfileKeyCiphertext {
    var newContents: [UInt8] = Array(repeating: 0, count: ProfileKeyCiphertext.SIZE)

    let ffi_return = FFI_PniCredentialPresentation_getProfileKeyCiphertext(self.contents, UInt32(self.contents.count), &newContents, UInt32(newContents.count))

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }

    do {
      return try ProfileKeyCiphertext(contents: newContents)
    } catch ZkGroupException.InvalidInput {
      throw ZkGroupException.AssertionError
    }

  }

  public func serialize() -> [UInt8] {
    return contents
  }

}
