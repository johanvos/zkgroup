//
// Copyright (C) 2020 Signal Messenger, LLC.
// All rights reserved.
//
// SPDX-License-Identifier: GPL-3.0-only
//

// Generated by zkgroup/codegen/codegen.py - do not edit

package org.signal.zkgroup.receipts;

import java.security.SecureRandom;
import org.signal.zkgroup.InvalidInputException;
import org.signal.zkgroup.ServerSecretParams;
import org.signal.zkgroup.VerificationFailedException;
import org.signal.zkgroup.ZkGroupError;
import org.signal.zkgroup.internal.Native;

public class ServerZkReceiptOperations {

  private final ServerSecretParams serverSecretParams;

  public ServerZkReceiptOperations(ServerSecretParams serverSecretParams) {
    this.serverSecretParams = serverSecretParams;
  }

  public ReceiptCredentialResponse issueReceiptCredential(ReceiptCredentialRequest receiptCredentialRequest, long receiptExpirationTime, long receiptLevel) throws VerificationFailedException {
    return issueReceiptCredential(new SecureRandom(), receiptCredentialRequest, receiptExpirationTime, receiptLevel);
  }

  public ReceiptCredentialResponse issueReceiptCredential(SecureRandom secureRandom, ReceiptCredentialRequest receiptCredentialRequest, long receiptExpirationTime, long receiptLevel) throws VerificationFailedException {
    byte[] newContents = new byte[ReceiptCredentialResponse.SIZE];
    byte[] random      = new byte[Native.RANDOM_LENGTH];

    secureRandom.nextBytes(random);

    int ffi_return = Native.serverSecretParamsIssueReceiptCredentialDeterministicJNI(serverSecretParams.getInternalContentsForJNI(), random, receiptCredentialRequest.getInternalContentsForJNI(), receiptExpirationTime, receiptLevel, newContents);
    if (ffi_return == Native.FFI_RETURN_INPUT_ERROR) {
      throw new VerificationFailedException();
    }

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw new ZkGroupError("FFI_RETURN!=OK");
    }

    try {
      return new ReceiptCredentialResponse(newContents);
    } catch (InvalidInputException e) {
      throw new AssertionError(e);
    }

  }

  public void verifyReceiptCredentialPresentation(ReceiptCredentialPresentation receiptCredentialPresentation) throws VerificationFailedException {
    int ffi_return = Native.serverSecretParamsVerifyReceiptCredentialPresentationJNI(serverSecretParams.getInternalContentsForJNI(), receiptCredentialPresentation.getInternalContentsForJNI());
    if (ffi_return == Native.FFI_RETURN_INPUT_ERROR) {
      throw new VerificationFailedException();
    }

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw new ZkGroupError("FFI_RETURN!=OK");
    }
  }

}
