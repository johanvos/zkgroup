
template_class = \
"""//
// Copyright (C) 2020 Signal Messenger, LLC.
// All rights reserved.
//
// SPDX-License-Identifier: GPL-3.0-only
//
// Generated by zkgroup/codegen/codegen.py - do not edit

%(imports)s

public class %(class_name)s : ByteArray {

  public static let SIZE: Int = %(size)s
%(static_methods)s%(constructors)s
%(methods)s%(serialize_method)s}
"""

template_constructor = \
"""
  public init(contents: %(constructor_contents_type)s) %(constructor_exception_decl)s {
    try super.init(newContents: %(constructor_contents)s, expectedLength: %(class_name)s.SIZE%(runtime_error_bool)s)
%(check_valid_contents)s
  }
"""

template_constructor_for_string_contents = \
"""
  public init(%(constructor_contents_type)s contents) %(constructor_exception_decl)s {
    try super.init(newContents: %(constructor_contents)s, expectedLength: %(class_name)s.SIZE%(runtime_error_bool)s)
%(check_valid_contents)s
  }
"""

serialize_method_string = \
"""
  public func serialize() throws -> String {
    do {
      return new String(contents.clone(), "UTF-8")
    } catch UnsupportedEncodingException e) {
      throw ZkGroupException.AssertionError
    }
  }

"""

serialize_method_binary = \
"""
  public func serialize() -> [UInt8] {
    return contents
  }

"""

template_wrapping_class = \
"""//
// Copyright (C) 2020 Signal Messenger, LLC.
// All rights reserved.
//
// SPDX-License-Identifier: GPL-3.0-only
//
// Generated by zkgroup/codegen/codegen.py - do not edit

%(imports)s

public class %(class_name)s {

  let %(wrapped_class_var)s: %(wrapped_class_type)s
%(static_methods)s
  public init(%(wrapped_class_var)s: %(wrapped_class_type)s) {
    self.%(wrapped_class_var)s = %(wrapped_class_var)s
  }
%(methods)s
}
"""

template_check_valid_contents_constructor = \
"""
    
    let ffi_return = FFI_%(class_name_camel)s_checkValidContents(self.contents, UInt32(self.contents.count))

    if (ffi_return == Native.FFI_RETURN_INPUT_ERROR) {
      throw ZkGroupException.InvalidInput
    }

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }"""

template_check_valid_contents_constructor_runtime_error = \
"""
    
    let ffi_return = FFI_%(class_name_camel)s_checkValidContents(self.contents, UInt32(self.contents.count))

    if (ffi_return == Native.FFI_RETURN_INPUT_ERROR) {
      throw ZkGroupException.IllegalArgument
    }

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }"""

template_static_method = \
"""
  %(access)s static func %(method_name)s(%(param_decls)s) %(exception_decl)s -> %(return_name)s {
    var newContents: [UInt8] = Array(repeating: 0, count: %(return_name)s.SIZE)%(get_rand)s

    let ffi_return = FFI_%(jni_method_name)s(%(param_args)s&newContents, UInt32(newContents.count))%(exception_check)s

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }

    do {
      return try %(return_name)s(contents: newContents)
    } catch ZkGroupException.Invalid {
      throw ZkGroupException.AssertionError
    }
  }
"""

template_static_method_retval_runtime_error_on_serialize = \
"""
  public static func %(method_name)s(%(param_decls)s) %(exception_decl)s -> %(return_name)s {
    var newContents: [UInt8] = Array(repeating: 0, count: %(return_name)s.SIZE)%(get_rand)s

    let ffi_return = FFI_%(jni_method_name)s(%(param_args)s&newContents, UInt32(newContents.count))%(exception_check)s

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }

    do {
      return try %(return_name)s(contents: newContents)
    } catch ZkGroupException.IllegalArgument {
      throw ZkGroupException.AssertionError
    } 
  }
"""

template_static_method_rand_wrapper = \
"""
  public static func %(method_name)s(%(param_decls)s) %(exception_decl)s -> %(return_name)s {
    var randomness: [UInt8] = Array(repeating: 0, count: Int(32))
    let result = SecRandomCopyBytes(kSecRandomDefault, randomness.count, &randomness)
    guard result == errSecSuccess else {
      throw ZkGroupException.AssertionError
    }

    return try %(full_method_name)s(%(param_args)s)
  }
"""

template_method = \
"""
  public func %(method_name)s(%(param_decls)s) %(exception_decl)s -> %(return_name)s {
    var newContents: [UInt8] = Array(repeating: 0, count: %(return_len)s)

    let ffi_return = FFI_%(jni_method_name)s(%(contents)s, %(param_args)s&newContents, UInt32(newContents.count))%(exception_check)s

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }

    do {
      return try %(return_name)s(contents: newContents)
    } catch ZkGroupException.InvalidInput {
      throw ZkGroupException.AssertionError
    }

  }
"""

template_method_retval_runtime_error_on_serialize = \
"""
  public func %(method_name)s(%(param_decls)s) %(exception_decl)s -> %(return_name)s {
    var newContents: [UInt8] = Array(repeating: 0, count: Int(%(return_len)s))%(get_rand)s

    let ffi_return = FFI_%(jni_method_name)s(%(contents)s, %(param_args)s&newContents, UInt32(newContents.count))%(exception_check)s

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }

    return try %(return_name)s(contents: newContents)
  }
"""

template_method_bool = \
"""
  public func %(method_name)s(%(param_decls)s) %(exception_decl)s{
    let ffi_return = FFI_%(jni_method_name)s(%(contents)s, %(param_args)s)%(exception_check)s

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }
  }
"""

template_method_uuid = \
"""
  public func %(method_name)s(%(param_decls)s) %(exception_decl)s -> %(return_name)s {
    var newContents: [UInt8] = Array(repeating: 0, count: Int(%(return_len)s))

    let ffi_return = FFI_%(jni_method_name)s(%(contents)s, %(param_args)s&newContents, UInt32(newContents.count))%(exception_check)s

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }

    return UUIDUtil.deserialize(newContents)
  }
"""

template_method_bytearray = \
"""
  public func %(method_name)s(%(param_decls)s) %(exception_decl)s -> [UInt8] {
    var newContents: [UInt8] = Array(repeating: 0, count: Int(%(return_len)s))

    let ffi_return = FFI_%(jni_method_name)s(%(contents)s, %(param_args)s&newContents, UInt32(newContents.count))%(exception_check)s

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
    }

    return newContents
  }
"""

template_method_int = \
"""
  public func %(method_name)s(%(param_decls)s) %(exception_decl)s -> UInt32 {
    var newContents: [UInt8] = Array(repeating: 0, count: Int(4))

    let ffi_return = FFI_%(jni_method_name)s(%(contents)s, %(param_args)s&newContents, UInt32(newContents.count))%(exception_check)s

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
     }

    let data = Data(bytes: newContents)
    let value = UInt32(bigEndian: data.withUnsafeBytes { $0.pointee })
    return value
  }
"""

template_method_long = \
"""
  public func %(method_name)s(%(param_decls)s) %(exception_decl)s -> UInt64 {
    var newContents: [UInt8] = Array(repeating: 0, count: Int(8))

    let ffi_return = FFI_%(jni_method_name)s(%(contents)s, %(param_args)s&newContents, UInt32(newContents.count))%(exception_check)s

    if (ffi_return != Native.FFI_RETURN_OK) {
      throw ZkGroupException.ZkGroupError
     }

    let data = Data(bytes: newContents)
    let value = UInt64(bigEndian: data.withUnsafeBytes { $0.pointee })
    return value
  }
"""

template_method_rand_wrapper = \
"""
  public func %(method_name)s(%(param_decls)s) %(exception_decl)s -> %(return_name)s {
    var randomness: [UInt8] = Array(repeating: 0, count: Int(32))
    let result = SecRandomCopyBytes(kSecRandomDefault, randomness.count, &randomness)
    guard result == errSecSuccess else {
      throw ZkGroupException.AssertionError
    }

    return try %(full_method_name)s(%(param_args)s)
  }
"""

def add_import(import_strings, class_dir_dict, my_dir_name, class_name):
    dir_name = class_dir_dict[class_name.snake()].snake()
    if len(dir_name)==0 and len(my_dir_name.snake()) == 0:
        return
    elif dir_name == my_dir_name.snake():
        return
    """
    if dir_name:
        import_strings.append("import org.signal.zkgroup.%s.%s;" % (dir_name, class_name.camel()))
    else:
        import_strings.append("import org.signal.zkgroup.%s;" % (class_name.camel()))
    """

def get_decls(params, import_strings, class_dir_dict, my_dir_name):
    s = ""
    for param in params:
        if param[1].snake() == "randomness":
            s += "randomness: [UInt8], "
            #SWIFT import_strings.append("import java.security.SecureRandom;")
        elif param[0] == "class":
            s += param[1].lower_camel() + ": " + param[1].camel() + ", "
            #SWIFT add_import(import_strings, class_dir_dict, my_dir_name, param[1])
        elif param[0] == "byte[]":
            s += param[1].lower_camel() + ": [UInt8], "
            #SWIFT add_import(import_strings, class_dir_dict, my_dir_name, param[1])
        elif param[0] == "int":
            s += param[1].lower_camel() + ": UInt32, "
            #SWIFT add_import(import_strings, class_dir_dict, my_dir_name, param[1])
        elif param[0] == "long":
            s += param[1].lower_camel() + ": UInt64, "
            #SWIFT add_import(import_strings, class_dir_dict, my_dir_name, param[1])
        elif param[0] == "UUID":
            s += param[1].lower_camel() + ": ZKGUuid, "
            #SWIFT add_import(import_strings, class_dir_dict, my_dir_name, param[1])
        else:
            s += param[1].lower_camel() + ": " + param[0] + ", "
    if len(s) != 0:
        s = s[:-2]
    return s

def get_rand_wrapper_decls(params):
    s = ""
    for param in params:
        if param[1].snake() != "randomness":
            if param[0] == "class":
                s += param[1].lower_camel() + ": " + param[1].camel() + ", "
            elif param[0] == "byte[]":
                s += param[1].lower_camel() + ": [UInt8], "
            elif param[0] == "int":
                s += param[1].lower_camel() + ": UInt32, "
            elif param[0] == "long":
                s += param[1].lower_camel() + ": UInt64, "
            elif param[0] == "UUID":
                s += param[1].lower_camel() + ": ZKGUuid, "
            else:
                s += param[1].lower_camel() + ": " + param[0] + ", "
    if len(s) != 0:
        s = s[:-2]
    return s


def get_args(params, import_strings, commaAtEnd):
    s = ""
    for param in params:
        if param[0] == "byte[]" or param[0] == "int" or param[0] == "long":
            term = param[1].lower_camel()
        # SWIFT elif param[0] == "UUID":
        # SWIFT    term = "UUIDUtil.serialize(" + param[1].lower_camel() + ")"
        elif param[1].snake() == "randomness":
            term = "randomness"
        else:
            term = param[1].lower_camel() + ".getInternalContentsForFFI()"

        if param[0] == "int" or param[0] == "long":
            s += term + ", "
        else:
            s += term + ", UInt32(" + term + ".count), "

    if len(s) != 0 and not commaAtEnd:
        s = s[:-2]
    return s

def get_jni_arg_decls(params, selfBool, commaAtEndBool):
    s = ""
    if selfBool:
        s += "byte[] self, "
    counter = 0
    for param in params:
        if param[0] == "byte[]":
            s += "byte[] %s, " % param[1].lower_camel()
        elif param[0] == "int":
            s += "int %s, " % param[1].lower_camel()
        elif param[0] == "long":
            s += "long %s, " % param[1].lower_camel()
        # elif param[0] == "UUID":
        #    s += "byte[] %s, " % param[1].lower_camel()
        elif param[1].snake() == "randomness":
            s += "byte[] %s, " % param[1].lower_camel()
        else:
            s += "byte[] %s, " % param[1].lower_camel()
        counter += 1

    if len(s) != 0 and not commaAtEndBool:
        s = s[:-2]

    if commaAtEndBool:
        s += "byte[] output"

    return s

def get_rand_wrapper_args(params, commaAtEnd):
    s = ""
    for param in params:
        if param[0] == "byte[]":
            s += param[1].lower_camel() + ": " + param[1].lower_camel() + ", "
        else:
            s += param[1].lower_camel() + ": " + param[1].lower_camel() + ", "
    if len(s) != 0 and not commaAtEnd:
        s = s[:-2]
    return s

def print_class(c, runtime_error_on_serialize_dict, class_dir_dict):
    static_methods_string = ""
    if len(c.methods) == 0 and len(c.static_methods) == 0:
        import_strings = []
    else:
        import_strings = [\
"import libzkgroup",
"import Foundation"
            ]

    my_dir_name = c.dir_name

    if c.wrap_class == None:
        contents = "self.contents"
    else:
        contents = c.wrap_class.lower_camel() + ".getInternalContentsForFFI()"
        add_import(import_strings, class_dir_dict, my_dir_name, c.wrap_class)
    contents += ", UInt32(%s.count)" % contents

    for method in c.static_methods:

        exception_decl = "throws "
        exception_check =""
        if len(method.params) > 1 or (len(method.params) == 1 and not method.method_name.snake().endswith("_deterministic")):
            if method.runtime_error == False:
                if method.verification == False:
                    #if my_dir_name.snake() != "":
                    #    import_strings.append("import org.signal.zkgroup.VerificationFailedException;")
                    exception_decl = "throws "
                    exception_check ="""\n    if (ffi_return == Native.FFI_RETURN_INPUT_ERROR) {
      throw ZkGroupException.VerificationFailed
    }"""
                else:
                    exception_decl = "throws VerificationFailed "
                    exception_check ="""\n    if (ffi_return == Native.FFI_RETURN_VERIFICATION_FAILED) {
      throw ZkGroupException.VerificationFailed
    }"""

        access = "public"
        method_name = method.method_name.lower_camel()
        get_rand = ""
        if method.method_name.snake().endswith("_deterministic"):
            method_name = method.method_name.lower_camel()[:-len("Deterministic")]
            param_args = get_rand_wrapper_args(method.params, False)
            get_rand = ""
            static_methods_string += template_static_method_rand_wrapper % {
                    "method_name": method_name,
                    "return_name": method.return_name.camel(),
                    "full_method_name": method_name,
                    "param_decls": get_rand_wrapper_decls(method.params),
                    "param_args": param_args,
                    "access": access,
                    "exception_decl": exception_decl,
                    "exception_check": exception_check,
                    }
        param_args = get_args(method.params, import_strings, True)
        if c.wrap_class == None:
            jni_method_name = c.class_name.camel() + "_" + method.method_name.lower_camel()
        else:
            jni_method_name = c.wrap_class.camel() + "_" + method.method_name.lower_camel()
        if runtime_error_on_serialize_dict[method.return_name.snake()]:
            template = template_static_method_retval_runtime_error_on_serialize
        else:
            template = template_static_method
        static_methods_string += template % {
                "method_name": method_name,
                "return_name": method.return_name.camel(),
                "return_len": c.class_len,
                "param_decls": get_decls(method.params, import_strings, class_dir_dict, my_dir_name),
                "param_args": param_args,
                "jni_method_name": jni_method_name, 
                "access": access,
                "exception_decl": exception_decl,
                "exception_check": exception_check,
                "get_rand": get_rand,
                }

    methods_string = ""
    for method in c.methods:

        if method.method_name.snake() == "check_valid_contents":
            continue

        exception_decl = "throws "
        exception_check =""
        if len(method.params) != 0:
            if method.runtime_error == False:
                if method.verification == False:
                    #if my_dir_name.snake() != "":
                    #    import_strings.append("import org.signal.zkgroup.VerificationFailedException;")
                    exception_decl = "throws "
                    exception_check ="""\n    if (ffi_return == Native.FFI_RETURN_INPUT_ERROR) {
      throw ZkGroupException.VerificationFailed
    }"""
                else:
                    exception_decl = "throws "
                    exception_check ="""\n    if (ffi_return == Native.FtFI_RETURN_VERIFICATION_FAILED) {
      throw ZkGroupException.VerificationFailed
    }"""

        access = "public"
        method_name = method.method_name.lower_camel()
        get_rand = ""
        if method.method_name.snake().endswith("_deterministic"):
            method_name = method.method_name.lower_camel()[:-len("Deterministic")]
            param_args = get_rand_wrapper_args(method.params, False)
            get_rand = """\n    byte[] random      = byte[Native.RANDOM_LENGTH];

    secureRandom.nextBytes(random);"""
            methods_string += template_method_rand_wrapper % {
                    "contents": contents,
                    "method_name": method_name,
                    "return_name": method.return_name.camel(),
                    "full_method_name": method_name,
                    "param_decls": get_rand_wrapper_decls(method.params),
                    "param_args": param_args,
                    "access": access,
                    "exception_decl": exception_decl,
                    "exception_check": exception_check,
                    }

        if c.wrap_class == None:
            jni_method_name = c.class_name.camel() + "_" + method.method_name.lower_camel()
        else:
            jni_method_name = c.wrap_class.camel()  + "_" + method.method_name.lower_camel()

        return_name = None
        return_len = None

        if method.return_type == "UUID":
            return_name = "ZKGUuid"
            return_len = "ZKGUuid.SIZE" 

        if method.return_type == "boolean":
            template = template_method_bool
            param_args = get_args(method.params, import_strings, False)
        elif method.return_type == "int":
            template = template_method_int
            param_args = get_args(method.params, import_strings, False)
        elif method.return_type == "long":
            template = template_method_long
            param_args = get_args(method.params, import_strings, False)
        elif method.return_type == "byte[]": # copied from UUID?
            template = template_method_bytearray
            param_args = get_args(method.params, import_strings, True)
            if method.relative_return_size is not None:
                return_len = f"{method.params[method.relative_return_size][1].lower_camel()}.count + {method.return_size_increment}"
        else:
            add_import(import_strings, class_dir_dict, my_dir_name, method.return_name)
            if runtime_error_on_serialize_dict[method.return_name.snake()]:
                template = template_method_retval_runtime_error_on_serialize
            else:
                template = template_method
            param_args = get_args(method.params, import_strings, True)
        if return_name is None:
            return_name = method.return_name.camel()
        if return_len is None:
            return_len = method.return_name.camel() + ".SIZE"


        methods_string += template % {
                "contents": contents,
                "method_name": method_name,
                "return_name": return_name,
                "return_len": return_len,
                "param_decls": get_decls(method.params, import_strings, class_dir_dict, my_dir_name),
                "param_args": param_args,
                "jni_method_name": jni_method_name, 
                "access": access,
                "exception_decl": exception_decl,
                "exception_check": exception_check,
                "get_rand": get_rand,
                }

    if c.dir_name.snake() != "":
        dir_section = "." + c.dir_name.snake()
    else:
        dir_section = ""

    constructor_exception_decl = "throws " # overwritten in needed
    runtime_error_bool = ""
    if c.check_valid_contents:
        if c.runtime_error_on_serialize:
            constructor_exception_decl = "throws " # overwritten in needed
            runtime_error_bool = ", unrecoverable: true"
            check_valid_contents = template_check_valid_contents_constructor_runtime_error % {
                    "class_name_camel": c.class_name.camel(), 
                    }
            jni_method_name = c.class_name.lower_camel() + "CheckValidContentsFFI"
        else:
            constructor_exception_decl = "throws " # overwritten in needed
            check_valid_contents = template_check_valid_contents_constructor % {
                    "class_name_camel": c.class_name.camel(), 
                    }
            jni_method_name = c.class_name.lower_camel() + "CheckValidContentsFFI"
    else:
        check_valid_contents = ""

    if c.no_serialize:
        constructor_access = "private"
    else:
        constructor_access = "public"

    import_strings = list(set(import_strings))
    import_strings.sort()

    # constructors
    constructors_string = ""
    constructor_contents = "contents"
    constructor_contents_type = "[UInt8]"
    constructors_string += template_constructor % {
        "class_name": c.class_name.camel(), 
        "constructor_contents": constructor_contents,
        "constructor_contents_type": constructor_contents_type,
        "constructor_access": constructor_access,
        "constructor_exception_decl": constructor_exception_decl,
        "runtime_error_bool": runtime_error_bool,
        "check_valid_contents": check_valid_contents,
        }

    # if c.string_contents == False:
    if True:
        serialize_method = serialize_method_binary
    else:
        constructor_contents = 'contents.getBytes("UTF-8")'
        constructor_contents_type = "String"
        serialize_method = serialize_method_string
        constructors_string += template_constructor_for_string_contents % {
            "class_name": c.class_name.camel(), 
            "constructor_contents": constructor_contents,
            "constructor_contents_type": constructor_contents_type,
            "constructor_access": constructor_access,
            "constructor_exception_decl": constructor_exception_decl + ", UnsupportedEncodingException",
            "runtime_error_bool": runtime_error_bool,
            "check_valid_contents": check_valid_contents,
            }
    constructors_string = constructors_string[:-1]

    if c.wrap_class != None:
        class_string = template_wrapping_class % {
                "imports": "\n".join(import_strings),
                "wrapped_class_type": c.wrap_class.camel(),
                "wrapped_class_var": c.wrap_class.lower_camel(), 
                "dir_section": dir_section,
                "class_name": c.class_name.camel(), 
                "size": c.class_len_int,
                "constructors": constructors_string,
                "static_methods": static_methods_string,
                "methods": methods_string,
                "serialize_method": serialize_method
                }
    else:
        class_string = template_class % {
                "imports": "\n".join(import_strings),
                "dir_section": dir_section,
                "class_name": c.class_name.camel(), 
                "size": c.class_len_int,
                "constructors": constructors_string,
                "static_methods": static_methods_string,
                "methods": methods_string,
                "serialize_method": serialize_method
                }
    return class_string

def produce_output(classes):

    runtime_error_on_serialize_dict = {}
    class_dir_dict = {}
    for c in classes:
        runtime_error_on_serialize_dict[c.class_name.snake()] = c.runtime_error_on_serialize
        class_dir_dict[c.class_name.snake()] = c.dir_name

    for c in classes:
        if c.no_class:
            continue
        f = open("swift/%s.swift" % c.class_name.camel(), "w")
        f.write(print_class(c, runtime_error_on_serialize_dict, class_dir_dict))
        f.close()
