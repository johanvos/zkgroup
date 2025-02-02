//
// Copyright (C) 2021 Signal Messenger, LLC.
// All rights reserved.
//
// SPDX-License-Identifier: GPL-3.0-only
//

#![allow(non_snake_case)]

use curve25519_dalek::scalar::Scalar;
use serde::{Deserialize, Serialize};

use crate::common::sho::Sho;
use crate::common::simple_types::ReceiptExpirationTime;
use crate::common::simple_types::ReceiptLevel;
use crate::common::simple_types::ReceiptSerialBytes;

/// The full set of information known by the client after receiving the credential response from
/// the issuing server. It will all be shared with the credential presentation. Initially the
/// client only knows the receipt_serial_bytes which is randomly generated. receipt_serial_bytes
/// should never be shared with the issuing service in unencrypted form.
///
/// Clients must do validation on the returned receipt_expiration_time and receipt_level to ensure
/// no tagging has occurred.
#[derive(Copy, Clone, PartialEq, Serialize, Deserialize)]
pub struct ReceiptStruct {
    pub(crate) receipt_serial_bytes: ReceiptSerialBytes,
    pub(crate) receipt_expiration_time: ReceiptExpirationTime,
    pub(crate) receipt_level: ReceiptLevel,
}

impl ReceiptStruct {
    pub fn new(
        receipt_serial_bytes: ReceiptSerialBytes,
        receipt_expiration_time: ReceiptExpirationTime,
        receipt_level: ReceiptLevel,
    ) -> Self {
        Self {
            receipt_serial_bytes,
            receipt_expiration_time,
            receipt_level,
        }
    }

    pub fn calc_m1(&self) -> Scalar {
        Self::calc_m1_from(self.receipt_expiration_time, self.receipt_level)
    }

    pub fn calc_m1_from(
        receipt_expiration_time: ReceiptExpirationTime,
        receipt_level: ReceiptLevel,
    ) -> Scalar {
        let mut bytes = [0u8; std::mem::size_of::<ReceiptExpirationTime>()
            + std::mem::size_of::<ReceiptLevel>()];
        bytes[..std::mem::size_of::<ReceiptExpirationTime>()]
            .copy_from_slice(&receipt_expiration_time.to_be_bytes());
        bytes[std::mem::size_of::<ReceiptExpirationTime>()..]
            .copy_from_slice(&receipt_level.to_be_bytes());
        let mut sho = Sho::new(b"Signal_ZKGroup_20210919_Receipt_CalcM1", &bytes);
        sho.get_scalar()
    }
}
